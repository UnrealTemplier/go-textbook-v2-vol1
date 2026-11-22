package main

import (
	"context"
	"errors"
	"flag"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	bookmarkflow "github.com/UnrealTemplier/go-textbook-v2-vol1/project/final"
)

func main() {
	cfg := bookmarkflow.ConfigFromEnv()
	flag.StringVar(&cfg.Addr, "addr", cfg.Addr, "HTTP listen address")
	flag.StringVar(&cfg.DataFile, "data", cfg.DataFile, "path to JSON bookmarks file")
	flag.IntVar(&cfg.CheckWorkers, "workers", cfg.CheckWorkers, "concurrent link-check workers")
	flag.Parse()

	logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))

	store, err := bookmarkflow.OpenFileStore(cfg.DataFile)
	if err != nil {
		logger.Error("не удалось открыть хранилище закладок", slog.Any("error", err))
		os.Exit(1)
	}

	checker := bookmarkflow.NewLinkChecker(&http.Client{Timeout: 5 * time.Second}, cfg.CheckWorkers)
	api := bookmarkflow.NewServer(store, checker, logger)

	srv := &http.Server{
		Addr:              cfg.Addr,
		Handler:           api,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	go func() {
		logger.Info("сервис BookmarkFlow запущен", slog.String("addr", cfg.Addr), slog.String("data", cfg.DataFile))
		if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			logger.Error("ошибка HTTP-сервера", slog.Any("error", err))
			stop()
		}
	}()

	<-ctx.Done()
	logger.Info("получен сигнал остановки, выполняем Graceful Shutdown")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), cfg.ShutdownTimeout)
	defer cancel()
	if err := srv.Shutdown(shutdownCtx); err != nil {
		logger.Error("ошибка корректной остановки", slog.Any("error", err))
		os.Exit(1)
	}
	logger.Info("сервис BookmarkFlow остановлен")
}
