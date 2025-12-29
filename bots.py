import asyncio
import time
from datetime import datetime
from playwright.async_api import async_playwright
import statistics

class ProgressTracker:
    def __init__(self, total):
        self.total = total
        self.completed = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            self.completed += 1
            if self.completed % 10 == 0 or self.completed == self.total:
                print(f"Progress: {self.completed}/{self.total} ({self.completed/self.total*100:.1f}%)")

async def send_request(browser, url, bot_id, progress_tracker, verbose=False):
    """Send a single HTTP request using Playwright and return the result"""
    context = None
    page = None
    
    try:
        if verbose and bot_id <= 5:
            print(f"[Bot {bot_id}] Starting...")
        
        start_time = time.time()
        
        # Create a new browser context (isolated session)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Create a new page
        page = await context.new_page()
        
        # Navigate to the URL
        response = await page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Get page information
        title = await page.title()
        current_url = page.url
        status = response.status if response else 'No Response'
        
        elapsed = time.time() - start_time
        
        if verbose and bot_id <= 5:
            print(f"[Bot {bot_id}] ✓ Status {status} ({elapsed:.2f}s) - {title[:40]}")
        
        result = {
            'bot_id': bot_id,
            'status': status,
            'elapsed': elapsed,
            'success': 200 <= status < 400 if isinstance(status, int) else False,
            'title': title[:50],
            'url': current_url
        }
        
        return result
        
    except Exception as e:
        elapsed = time.time() - start_time
        error_msg = str(e)
        
        if verbose and bot_id <= 5:
            print(f"[Bot {bot_id}] ✗ Error: {error_msg[:60]}")
        
        return {
            'bot_id': bot_id,
            'status': 'Error',
            'elapsed': elapsed,
            'success': False,
            'error': error_msg[:200]
        }
        
    finally:
        # Clean up
        if page:
            await page.close()
        if context:
            await context.close()
        
        await progress_tracker.increment()

async def simulate_concurrent_requests(url, num_bots=100, max_concurrent=50, verbose=False, headless=True):
    """Simulate multiple bots hitting a site concurrently using Playwright"""
    print(f"\n{'='*70}")
    print(f"🔬 PLAYWRIGHT LOAD TEST CONFIGURATION")
    print(f"{'='*70}")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target URL: {url}")
    print(f"🤖 Number of bots: {num_bots}")
    print(f"🔧 Max concurrent browsers: {max_concurrent}")
    print(f"👁️  Headless mode: {headless}")
    print(f"{'='*70}\n")
    
    progress_tracker = ProgressTracker(num_bots)
    
    print(f"🚀 Launching {num_bots} concurrent requests...")
    print("-" * 70)
    
    start_time = time.time()
    results = []
    
    async with async_playwright() as p:
        # Launch browser (reuse single browser instance)
        browser = await p.chromium.launch(headless=headless)
        
        # Create semaphore to limit concurrent operations
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_request(bot_id):
            async with semaphore:
                return await send_request(browser, url, bot_id, progress_tracker, verbose)
        
        # Execute all requests concurrently
        tasks = [limited_request(i) for i in range(1, num_bots + 1)]
        results = await asyncio.gather(*tasks)
        
        await browser.close()
    
    total_time = time.time() - start_time
    
    print("-" * 70)
    print(f"✓ All requests completed!\n")
    
    # Analyze results
    successful = sum(1 for r in results if r['success'])
    failed = num_bots - successful
    
    if not results:
        print("No results to analyze!")
        return results
    
    elapsed_times = [r['elapsed'] for r in results]
    avg_response_time = statistics.mean(elapsed_times)
    median_time = statistics.median(elapsed_times)
    min_time = min(elapsed_times)
    max_time = max(elapsed_times)
    
    # Calculate percentiles
    sorted_times = sorted(elapsed_times)
    p90_time = sorted_times[int(len(sorted_times) * 0.9)]
    p95_time = sorted_times[int(len(sorted_times) * 0.95)]
    p99_time = sorted_times[int(len(sorted_times) * 0.99)]
    
    status_codes = {}
    for r in results:
        status = r['status']
        status_codes[status] = status_codes.get(status, 0) + 1
    
    # Print detailed summary
    print(f"{'='*70}")
    print(f"📊 LOAD TEST RESULTS")
    print(f"{'='*70}")
    print(f"\n⏱️  TIMING METRICS:")
    print(f"   Total duration: {total_time:.2f} seconds")
    print(f"   Throughput: {num_bots/total_time:.2f} requests/second")
    
    print(f"\n✅ SUCCESS RATE:")
    print(f"   Successful: {successful}/{num_bots} ({successful/num_bots*100:.1f}%)")
    print(f"   Failed: {failed}/{num_bots} ({failed/num_bots*100:.1f}%)")
    
    print(f"\n⏲️  RESPONSE TIME STATISTICS:")
    print(f"   Average:  {avg_response_time:.3f}s")
    print(f"   Median:   {median_time:.3f}s")
    print(f"   Min:      {min_time:.3f}s")
    print(f"   Max:      {max_time:.3f}s")
    print(f"   P90:      {p90_time:.3f}s")
    print(f"   P95:      {p95_time:.3f}s")
    print(f"   P99:      {p99_time:.3f}s")
    
    print(f"\n📈 STATUS DISTRIBUTION:")
    for status, count in sorted(status_codes.items(), key=lambda x: str(x[0])):
        percentage = (count/num_bots) * 100
        bar_length = int(percentage / 2.5)  # Scale to 40 chars max
        bar = '█' * bar_length
        print(f"   {str(status):12} {count:4} ({percentage:5.1f}%) {bar}")
    
    print(f"\n{'='*70}")
    
    return results

async def main():
    print(f"{'='*70}")
    print(f"🌐 PLAYWRIGHT LOAD TESTING TOOL")
    print(f"{'='*70}")
    print(f"\n⚠️  LEGAL WARNING:")
    print(f"   Only test websites you own or have explicit permission to test.")
    print(f"   Unauthorized load testing may violate laws and terms of service.")
    print(f"\n💻 FEATURES:")
    print(f"   - Fast async/await architecture")
    print(f"   - Real browser contexts (Chrome/Firefox/Safari)")
    print(f"   - Efficient resource usage with context reuse")
    print(f"   - Supports 100s-1000s of concurrent requests")
    print(f"\n📦 SETUP:")
    print(f"   pip install playwright")
    print(f"   playwright install chromium")
    print(f"{'='*70}")
    
    # Configuration
    target_url = "https://aim.knust.edu.gh/"
    num_bots = 10000  # Playwright can handle much more!
    max_concurrent = 1000  # Number of concurrent browser contexts
    verbose = True  # Show logs for first 5 bots
    headless = True  # Run in headless mode (faster)
    
    # Run the test
    results = await simulate_concurrent_requests(
        url=target_url,
        num_bots=num_bots,
        max_concurrent=max_concurrent,
        verbose=verbose,
        headless=headless
    )
    
    # Show error details if any
    failures = [r for r in results if not r['success']]
    if failures:
        print(f"\n❌ ERROR DETAILS (First 10):")
        print("-" * 70)
        
        # Group errors by type
        error_groups = {}
        for f in failures:
            error_msg = f.get('error', 'Unknown error')
            # Get first line of error for grouping
            error_type = error_msg.split('\n')[0][:80]
            if error_type not in error_groups:
                error_groups[error_type] = []
            error_groups[error_type].append(f['bot_id'])
        
        for error_type, bot_ids in list(error_groups.items())[:10]:
            print(f"   {error_type}")
            print(f"   → Bots: {bot_ids[:10]}{' ...' if len(bot_ids) > 10 else ''} ({len(bot_ids)} total)")
            print()
        
        if len(error_groups) > 10:
            print(f"   ... and {len(error_groups)-10} more error types")
    
    print(f"\n✨ Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    asyncio.run(main())