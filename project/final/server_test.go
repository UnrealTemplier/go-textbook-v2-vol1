package bookmarkflow

import (
	"bytes"
	"encoding/json"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"strings"
	"testing"
)

func TestBookmarkFlowHTTPCRUDAndPersistence(t *testing.T) {
	dataPath := filepath.Join(t.TempDir(), "bookmarks.json")
	store, err := OpenFileStore(dataPath)
	if err != nil {
		t.Fatalf("OpenFileStore failed: %v", err)
	}
	srv := NewServer(store, nil, slog.New(slog.DiscardHandler))

	// 1. Healthcheck + проверка X-Request-ID
	rec := httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/healthz", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("GET /healthz status = %d, want 200", rec.Code)
	}
	if rec.Header().Get("X-Request-ID") == "" {
		t.Fatal("missing X-Request-ID response header")
	}

	// 2. Создание закладки (POST)
	body := `{"title":"Go Documentation","url":"https://go.dev/doc","tags":["Go","docs"]}`
	rec = httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodPost, "/api/v1/bookmarks", strings.NewReader(body)))
	if rec.Code != http.StatusCreated {
		t.Fatalf("POST status = %d, body = %s", rec.Code, rec.Body.String())
	}
	var created Bookmark
	if err := json.Unmarshal(rec.Body.Bytes(), &created); err != nil {
		t.Fatalf("unmarshal created: %v", err)
	}
	if created.ID != 1 || created.Title != "Go Documentation" {
		t.Fatalf("unexpected created bookmark: %+v", created)
	}

	// 3. Фильтрация по тегу (GET ?tag=docs)
	rec = httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/api/v1/bookmarks?tag=docs", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("GET list status = %d", rec.Code)
	}
	var listResp struct {
		Items []Bookmark `json:"items"`
		Count int        `json:"count"`
	}
	if err := json.Unmarshal(rec.Body.Bytes(), &listResp); err != nil {
		t.Fatalf("unmarshal list: %v", err)
	}
	if listResp.Count != 1 {
		t.Fatalf("list count = %d, want 1", listResp.Count)
	}

	// 4. Обновление закладки (PUT)
	updBody := `{"title":"Official Go Docs","url":"https://go.dev/doc","tags":["go","reference"]}`
	rec = httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodPut, "/api/v1/bookmarks/1", strings.NewReader(updBody)))
	if rec.Code != http.StatusOK {
		t.Fatalf("PUT status = %d, body = %s", rec.Code, rec.Body.String())
	}

	// 5. Проверка перезагрузки файла с диска
	reloadedStore, err := OpenFileStore(dataPath)
	if err != nil {
		t.Fatalf("reload FileStore failed: %v", err)
	}
	got, err := reloadedStore.Get(1)
	if err != nil || got.Title != "Official Go Docs" {
		t.Fatalf("reloaded Get(1) = (%+v, %v)", got, err)
	}

	// 6. Удаление (DELETE) и проверка 404
	rec = httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodDelete, "/api/v1/bookmarks/1", nil))
	if rec.Code != http.StatusNoContent {
		t.Fatalf("DELETE status = %d, want 204", rec.Code)
	}

	rec = httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/api/v1/bookmarks/1", nil))
	if rec.Code != http.StatusNotFound {
		t.Fatalf("GET deleted status = %d, want 404", rec.Code)
	}
}

func TestBookmarkFlowValidationAndErrorCases(t *testing.T) {
	store, err := OpenFileStore(filepath.Join(t.TempDir(), "b.json"))
	if err != nil {
		t.Fatalf("OpenFileStore failed: %v", err)
	}
	srv := NewServer(store, nil, slog.New(slog.DiscardHandler))

	tests := []struct {
		name       string
		method     string
		target     string
		body       string
		wantStatus int
	}{
		{
			name:       "invalid json syntax",
			method:     http.MethodPost,
			target:     "/api/v1/bookmarks",
			body:       `{"title":`,
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "unknown field rejected",
			method:     http.MethodPost,
			target:     "/api/v1/bookmarks",
			body:       `{"title":"Go","url":"https://go.dev","extra":1}`,
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "invalid url scheme",
			method:     http.MethodPost,
			target:     "/api/v1/bookmarks",
			body:       `{"title":"Go","url":"ftp://go.dev"}`,
			wantStatus: http.StatusUnprocessableEntity,
		},
		{
			name:       "invalid path id",
			method:     http.MethodGet,
			target:     "/api/v1/bookmarks/not-a-number",
			wantStatus: http.StatusBadRequest,
		},
		{
			name:       "not found id",
			method:     http.MethodGet,
			target:     "/api/v1/bookmarks/999",
			wantStatus: http.StatusNotFound,
		},
	}

	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			rec := httptest.NewRecorder()
			req := httptest.NewRequest(tc.method, tc.target, strings.NewReader(tc.body))
			srv.ServeHTTP(rec, req)
			if rec.Code != tc.wantStatus {
				t.Fatalf("got status %d, want %d (body: %s)", rec.Code, tc.wantStatus, rec.Body.String())
			}
		})
	}
}

func TestBookmarkFlowCheckEndpointOffline(t *testing.T) {
	// Поднимаем локальный тестовый сервер — тест на 100% автономен и не ходит в Интернет.
	targetMux := http.NewServeMux()
	targetMux.HandleFunc("/ok", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusOK)
	})
	targetMux.HandleFunc("/missing", func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	})
	targetSrv := httptest.NewServer(targetMux)
	defer targetSrv.Close()

	store, err := OpenFileStore(filepath.Join(t.TempDir(), "check.json"))
	if err != nil {
		t.Fatalf("OpenFileStore failed: %v", err)
	}
	if _, err := store.Create(CreateInput{Title: "OK Page", URL: targetSrv.URL + "/ok"}); err != nil {
		t.Fatalf("create ok bookmark: %v", err)
	}
	if _, err := store.Create(CreateInput{Title: "Missing Page", URL: targetSrv.URL + "/missing"}); err != nil {
		t.Fatalf("create missing bookmark: %v", err)
	}

	checker := NewLinkChecker(targetSrv.Client(), 2)
	srv := NewServer(store, checker, slog.New(slog.DiscardHandler))

	rec := httptest.NewRecorder()
	srv.ServeHTTP(rec, httptest.NewRequest(http.MethodPost, "/api/v1/bookmarks/check", nil))
	if rec.Code != http.StatusOK {
		t.Fatalf("POST /check status = %d, body = %s", rec.Code, rec.Body.String())
	}

	var resp struct {
		Results []CheckResult `json:"results"`
		Count   int           `json:"count"`
	}
	if err := json.Unmarshal(rec.Body.Bytes(), &resp); err != nil {
		t.Fatalf("unmarshal check response: %v", err)
	}
	if resp.Count != 2 {
		t.Fatalf("count = %d, want 2", resp.Count)
	}
	if !resp.Results[0].Reachable || resp.Results[0].StatusCode != http.StatusOK {
		t.Fatalf("result[0] = %+v, want reachable 200", resp.Results[0])
	}
	if resp.Results[1].Reachable || resp.Results[1].StatusCode != http.StatusNotFound {
		t.Fatalf("result[1] = %+v, want unreachable 404", resp.Results[1])
	}
}

func TestRecoverMiddleware(t *testing.T) {
	panicking := http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		panic("unexpected bug")
	})
	h := Chain(panicking, RequestIDMiddleware(), RecoverMiddleware(slog.New(slog.DiscardHandler)))

	rec := httptest.NewRecorder()
	h.ServeHTTP(rec, httptest.NewRequest(http.MethodGet, "/boom", nil))
	if rec.Code != http.StatusInternalServerError {
		t.Fatalf("status = %d, want 500", rec.Code)
	}
	if !bytes.Contains(rec.Body.Bytes(), []byte("внутренняя ошибка сервера")) {
		t.Fatalf("unexpected recover body: %s", rec.Body.String())
	}
}
