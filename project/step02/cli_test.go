package step02

import (
	"bytes"
	"errors"
	"strings"
	"testing"
)

func TestAppLifecycle(t *testing.T) {
	app := NewApp()
	var buf bytes.Buffer

	if err := app.Execute([]string{"add", "Go Standard Library", "https://pkg.go.dev/std"}, &buf); err != nil {
		t.Fatalf("add #1 failed: %v", err)
	}
	if err := app.Execute([]string{"add", "Go Spec", "https://go.dev/ref/spec"}, &buf); err != nil {
		t.Fatalf("add #2 failed: %v", err)
	}

	buf.Reset()
	if err := app.Execute([]string{"search", "spec"}, &buf); err != nil {
		t.Fatalf("search failed: %v", err)
	}
	if !strings.Contains(buf.String(), "Go Spec") || strings.Contains(buf.String(), "Standard Library") {
		t.Fatalf("unexpected search output:\n%s", buf.String())
	}

	buf.Reset()
	if err := app.Execute([]string{"delete", "1"}, &buf); err != nil {
		t.Fatalf("delete failed: %v", err)
	}

	buf.Reset()
	if err := app.Execute([]string{"list"}, &buf); err != nil {
		t.Fatalf("list failed: %v", err)
	}
	if strings.Contains(buf.String(), "Standard Library") || !strings.Contains(buf.String(), "Go Spec") {
		t.Fatalf("unexpected list after delete:\n%s", buf.String())
	}
}

func TestAppErrors(t *testing.T) {
	app := NewApp()
	tests := []struct {
		name    string
		args    []string
		wantErr error
	}{
		{name: "no args", args: nil, wantErr: ErrInvalidArgs},
		{name: "unknown cmd", args: []string{"export"}, wantErr: ErrUnknownCommand},
		{name: "bad add args", args: []string{"add", "only-title"}, wantErr: ErrInvalidArgs},
		{name: "empty title", args: []string{"add", " ", "https://go.dev"}, wantErr: ErrEmptyTitle},
		{name: "bad url", args: []string{"add", "Go", "not-a-url"}, wantErr: ErrInvalidURL},
		{name: "bad delete id", args: []string{"delete", "abc"}, wantErr: ErrInvalidArgs},
		{name: "missing id", args: []string{"delete", "42"}, wantErr: ErrNotFound},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			var buf bytes.Buffer
			err := app.Execute(tc.args, &buf)
			if !errors.Is(err, tc.wantErr) {
				t.Fatalf("got error %v, want %v", err, tc.wantErr)
			}
		})
	}
}
