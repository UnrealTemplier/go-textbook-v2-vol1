package step01

import (
	"bytes"
	"errors"
	"strings"
	"testing"
)

func TestAddBookmarkAndPrintList(t *testing.T) {
	var titles, urls []string
	var err error

	titles, urls, err = AddBookmark(titles, urls, "  Документация Go  ", "https://go.dev/doc")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	titles, urls, err = AddBookmark(titles, urls, "Блог Go", "https://go.dev/blog")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	var buf bytes.Buffer
	if err := PrintList(&buf, titles, urls); err != nil {
		t.Fatalf("PrintList failed: %v", err)
	}

	got := buf.String()
	wantLines := []string{
		"#1 | Документация Go -> https://go.dev/doc",
		"#2 | Блог Go -> https://go.dev/blog",
	}
	for _, want := range wantLines {
		if !strings.Contains(got, want) {
			t.Errorf("output %q does not contain %q", got, want)
		}
	}
}

func TestAddBookmarkValidation(t *testing.T) {
	tests := []struct {
		name    string
		title   string
		url     string
		wantErr error
	}{
		{name: "empty title", title: "   ", url: "https://go.dev", wantErr: ErrEmptyTitle},
		{name: "missing scheme", title: "Go", url: "go.dev", wantErr: ErrInvalidURL},
		{name: "ftp scheme", title: "FTP", url: "ftp://example.com", wantErr: ErrInvalidURL},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			_, _, err := AddBookmark(nil, nil, tc.title, tc.url)
			if !errors.Is(err, tc.wantErr) {
				t.Fatalf("got error %v, want %v", err, tc.wantErr)
			}
		})
	}
}

func TestPrintEmptyList(t *testing.T) {
	var buf bytes.Buffer
	if err := PrintList(&buf, nil, nil); err != nil {
		t.Fatalf("PrintList failed: %v", err)
	}
	if !strings.Contains(buf.String(), "Список закладок пуст.") {
		t.Fatalf("unexpected empty output: %q", buf.String())
	}
}
