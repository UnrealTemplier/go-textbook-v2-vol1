package step05

import (
	"context"
	"errors"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestCheckAllWorkerPoolLimit(t *testing.T) {
	store := NewSafeStore()
	for range 10 {
		store.Add("Link", "https://example.com")
	}

	var active atomic.Int32
	var peak atomic.Int32

	probe := func(ctx context.Context, rawURL string) (bool, error) {
		cur := active.Add(1)
		for {
			prev := peak.Load()
			if cur <= prev || peak.CompareAndSwap(prev, cur) {
				break
			}
		}
		defer active.Add(-1)

		select {
		case <-ctx.Done():
			return false, ctx.Err()
		case <-time.After(5 * time.Millisecond):
			return true, nil
		}
	}

	const maxWorkers = 3
	results := CheckAll(context.Background(), store.List(), maxWorkers, probe, nil)
	if len(results) != 10 {
		t.Fatalf("got %d results, want 10", len(results))
	}
	for i, r := range results {
		if !r.OK || r.Err != nil || r.BookmarkID != i+1 {
			t.Fatalf("unexpected result[%d]: %+v", i, r)
		}
	}
	if peak.Load() > maxWorkers {
		t.Fatalf("worker pool limit exceeded: peak=%d, limit=%d", peak.Load(), maxWorkers)
	}
}

func TestCheckAllRespectsContextCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()

	bookmarks := []Bookmark{
		{ID: 1, Title: "A", URL: "https://a.example"},
		{ID: 2, Title: "B", URL: "https://b.example"},
	}
	probe := func(ctx context.Context, _ string) (bool, error) {
		return false, ctx.Err()
	}

	results := CheckAll(ctx, bookmarks, 2, probe, nil)
	for _, r := range results {
		if r.OK || !errors.Is(r.Err, context.Canceled) {
			t.Fatalf("expected context.Canceled, got %+v", r)
		}
	}
}

func TestSafeStoreConcurrentAccess(t *testing.T) {
	store := NewSafeStore()
	var wg sync.WaitGroup
	for range 8 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range 25 {
				store.Add("Concurrent", "https://go.dev")
				_ = store.List()
			}
		}()
	}
	wg.Wait()

	if got := len(store.List()); got != 200 {
		t.Fatalf("got %d bookmarks, want 200", got)
	}
}
