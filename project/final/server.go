package bookmarkflow

import (
	"encoding/json"
	"errors"
	"io"
	"log/slog"
	"net/http"
	"strconv"
)

const maxBodyBytes = 1 << 20 // 1 МиБ — защита от бесконтрольно больших JSON-тел

// Server объединяет HTTP-маршрутизацию, хранилище закладок и чекер ссылок.
type Server struct {
	store   Store
	checker *LinkChecker
	logger  *slog.Logger
	handler http.Handler
}

// NewServer собирает http.ServeMux (Go 1.22+) с цепочкой middleware.
func NewServer(store Store, checker *LinkChecker, logger *slog.Logger) *Server {
	if logger == nil {
		logger = slog.New(slog.DiscardHandler)
	}
	if checker == nil {
		checker = NewLinkChecker(nil, 4)
	}

	s := &Server{
		store:   store,
		checker: checker,
		logger:  logger,
	}

	mux := http.NewServeMux()
	mux.HandleFunc("GET /healthz", s.handleHealth)
	mux.HandleFunc("GET /api/v1/bookmarks", s.handleList)
	mux.HandleFunc("POST /api/v1/bookmarks", s.handleCreate)
	mux.HandleFunc("GET /api/v1/bookmarks/{id}", s.handleGet)
	mux.HandleFunc("PUT /api/v1/bookmarks/{id}", s.handleUpdate)
	mux.HandleFunc("DELETE /api/v1/bookmarks/{id}", s.handleDelete)
	mux.HandleFunc("POST /api/v1/bookmarks/check", s.handleCheckAll)

	s.handler = Chain(
		mux,
		RequestIDMiddleware(),
		LoggingMiddleware(logger),
		RecoverMiddleware(logger),
	)
	return s
}

// ServeHTTP позволяет передавать *Server напрямую в http.Server и httptest.
func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	s.handler.ServeHTTP(w, r)
}

func (s *Server) handleHealth(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (s *Server) handleList(w http.ResponseWriter, r *http.Request) {
	filter := ListFilter{
		Tag:   r.URL.Query().Get("tag"),
		Query: r.URL.Query().Get("q"),
	}
	items, err := s.store.List(filter)
	if err != nil {
		writeJSONError(w, http.StatusInternalServerError, "не удалось получить список закладок")
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": items, "count": len(items)})
}

func (s *Server) handleCreate(w http.ResponseWriter, r *http.Request) {
	var in CreateInput
	if !decodeJSONBody(w, r, &in) {
		return
	}
	created, err := s.store.Create(in)
	if err != nil {
		s.writeStoreError(w, err)
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (s *Server) handleGet(w http.ResponseWriter, r *http.Request) {
	id, ok := parseIDParam(w, r)
	if !ok {
		return
	}
	bm, err := s.store.Get(id)
	if err != nil {
		s.writeStoreError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, bm)
}

func (s *Server) handleUpdate(w http.ResponseWriter, r *http.Request) {
	id, ok := parseIDParam(w, r)
	if !ok {
		return
	}
	var in UpdateInput
	if !decodeJSONBody(w, r, &in) {
		return
	}
	updated, err := s.store.Update(id, in)
	if err != nil {
		s.writeStoreError(w, err)
		return
	}
	writeJSON(w, http.StatusOK, updated)
}

func (s *Server) handleDelete(w http.ResponseWriter, r *http.Request) {
	id, ok := parseIDParam(w, r)
	if !ok {
		return
	}
	if err := s.store.Delete(id); err != nil {
		s.writeStoreError(w, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (s *Server) handleCheckAll(w http.ResponseWriter, r *http.Request) {
	items, err := s.store.List(ListFilter{})
	if err != nil {
		writeJSONError(w, http.StatusInternalServerError, "не удалось загрузить закладки для проверки")
		return
	}
	results := s.checker.CheckAll(r.Context(), items)
	writeJSON(w, http.StatusOK, map[string]any{"results": results, "count": len(results)})
}

func (s *Server) writeStoreError(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, ErrValidation):
		writeJSONError(w, http.StatusUnprocessableEntity, err.Error())
	case errors.Is(err, ErrNotFound):
		writeJSONError(w, http.StatusNotFound, err.Error())
	default:
		s.logger.Error("store error", slog.Any("error", err))
		writeJSONError(w, http.StatusInternalServerError, "внутренняя ошибка хранилища")
	}
}

func parseIDParam(w http.ResponseWriter, r *http.Request) (int, bool) {
	raw := r.PathValue("id")
	id, err := strconv.Atoi(raw)
	if err != nil || id <= 0 {
		writeJSONError(w, http.StatusBadRequest, "идентификатор id должен быть положительным целым числом")
		return 0, false
	}
	return id, true
}

func decodeJSONBody(w http.ResponseWriter, r *http.Request, dst any) bool {
	r.Body = http.MaxBytesReader(w, r.Body, maxBodyBytes)
	dec := json.NewDecoder(r.Body)
	dec.DisallowUnknownFields()

	if err := dec.Decode(dst); err != nil {
		var maxErr *http.MaxBytesError
		if errors.As(err, &maxErr) {
			writeJSONError(w, http.StatusRequestEntityTooLarge, "размер тела запроса превышает 1 МиБ")
			return false
		}
		writeJSONError(w, http.StatusBadRequest, "некорректный JSON в теле запроса")
		return false
	}
	if err := dec.Decode(&struct{}{}); !errors.Is(err, io.EOF) {
		writeJSONError(w, http.StatusBadRequest, "тело запроса должно содержать ровно один JSON-объект")
		return false
	}
	return true
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func writeJSONError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}
