package bookmarkflow

import (
	"context"
	"net/http"
	"sync"
	"time"
)

// CheckResult описывает итог HTTP-проверки одной закладки.
type CheckResult struct {
	BookmarkID int    `json:"bookmark_id"`
	URL        string `json:"url"`
	Reachable  bool   `json:"reachable"`
	StatusCode int    `json:"status_code,omitempty"`
	LatencyMS  int64  `json:"latency_ms"`
	Error      string `json:"error,omitempty"`
}

// LinkChecker конкурентно проверяет доступность закладок по HTTP с ограничением числа воркеров.
type LinkChecker struct {
	client  *http.Client
	workers int
}

// NewLinkChecker создаёт чекер с заданным HTTP-клиентом и количеством воркеров.
func NewLinkChecker(client *http.Client, workers int) *LinkChecker {
	if client == nil {
		client = &http.Client{Timeout: 5 * time.Second}
	}
	return &LinkChecker{
		client:  client,
		workers: max(workers, 1),
	}
}

// CheckAll проверяет переданные закладки пулом воркеров, сохраняя порядок результатов.
func (c *LinkChecker) CheckAll(ctx context.Context, items []Bookmark) []CheckResult {
	if len(items) == 0 {
		return []CheckResult{}
	}

	type job struct {
		idx int
		bm  Bookmark
	}

	workers := min(c.workers, len(items))
	jobs := make(chan job)
	results := make([]CheckResult, len(items))

	var wg sync.WaitGroup
	for range workers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := range jobs {
				results[j.idx] = c.checkOne(ctx, j.bm)
			}
		}()
	}

	for i, bm := range items {
		select {
		case <-ctx.Done():
			results[i] = CheckResult{
				BookmarkID: bm.ID,
				URL:        bm.URL,
				Reachable:  false,
				Error:      ctx.Err().Error(),
			}
		case jobs <- job{idx: i, bm: bm}:
		}
	}
	close(jobs)
	wg.Wait()

	return results
}

func (c *LinkChecker) checkOne(ctx context.Context, bm Bookmark) CheckResult {
	start := time.Now()
	req, err := http.NewRequestWithContext(ctx, http.MethodHead, bm.URL, nil)
	if err != nil {
		return CheckResult{
			BookmarkID: bm.ID,
			URL:        bm.URL,
			LatencyMS:  time.Since(start).Milliseconds(),
			Error:      err.Error(),
		}
	}

	resp, err := c.client.Do(req)
	if err != nil {
		return CheckResult{
			BookmarkID: bm.ID,
			URL:        bm.URL,
			LatencyMS:  time.Since(start).Milliseconds(),
			Error:      err.Error(),
		}
	}
	defer resp.Body.Close()

	return CheckResult{
		BookmarkID: bm.ID,
		URL:        bm.URL,
		Reachable:  resp.StatusCode >= 200 && resp.StatusCode < 400,
		StatusCode: resp.StatusCode,
		LatencyMS:  time.Since(start).Milliseconds(),
	}
}
