package step07

import (
	"slices"
	"testing"
)

func TestTagIndexAndIntersection(t *testing.T) {
	idx := NewTagIndex()
	items := []Bookmark{
		{ID: 3, Title: "Net/HTTP", URL: "https://pkg.go.dev/net/http", Tags: []string{"go", "backend", "http"}},
		{ID: 1, Title: "Go Spec", URL: "https://go.dev/ref/spec", Tags: []string{"Go", "docs"}},
		{ID: 2, Title: "Testing", URL: "https://pkg.go.dev/testing", Tags: []string{"go", "backend"}},
	}
	for _, it := range items {
		idx.Index(it)
	}

	if got := idx.FindByTag("go"); !slices.Equal(got, []int{1, 2, 3}) {
		t.Fatalf("FindByTag(go) = %v, want [1 2 3]", got)
	}
	if got := idx.FindByAllTags("go", "backend"); !slices.Equal(got, []int{2, 3}) {
		t.Fatalf("FindByAllTags(go, backend) = %v, want [2 3]", got)
	}
	if got := idx.FindByAllTags("go", "backend", "http"); !slices.Equal(got, []int{3}) {
		t.Fatalf("FindByAllTags(go, backend, http) = %v, want [3]", got)
	}

	idx.Remove(2, []string{"go", "backend"})
	if got := idx.FindByAllTags("go", "backend"); !slices.Equal(got, []int{3}) {
		t.Fatalf("after Remove(2): got %v, want [3]", got)
	}
}

func TestBinarySearchByIDAndSortByTitle(t *testing.T) {
	sorted := []Bookmark{
		{ID: 2, Title: "Zeta"},
		{ID: 5, Title: "alpha"},
		{ID: 9, Title: "Beta"},
	}

	got, ok := BinarySearchByID(sorted, 5)
	if !ok || got.Title != "alpha" {
		t.Fatalf("BinarySearchByID(5) = (%+v, %v)", got, ok)
	}
	if _, ok := BinarySearchByID(sorted, 7); ok {
		t.Fatal("BinarySearchByID(7) unexpectedly found an item")
	}

	byTitle := SortByTitle(sorted)
	wantOrder := []int{5, 9, 2}
	for i, wantID := range wantOrder {
		if byTitle[i].ID != wantID {
			t.Fatalf("SortByTitle[%d].ID = %d, want %d", i, byTitle[i].ID, wantID)
		}
	}
}
