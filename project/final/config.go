package bookmarkflow

import (
	"os"
	"strconv"
	"time"
)

// Config хранит настройки HTTP-сервиса BookmarkFlow.
type Config struct {
	Addr            string
	DataFile        string
	CheckWorkers    int
	ShutdownTimeout time.Duration
}

// ConfigFromEnv читает конфигурацию из переменных окружения с безопасными значениями по умолчанию.
func ConfigFromEnv() Config {
	cfg := Config{
		Addr:            envOrDefault("BOOKMARKFLOW_ADDR", ":8080"),
		DataFile:        envOrDefault("BOOKMARKFLOW_DATA_FILE", "bookmarks.json"),
		CheckWorkers:    4,
		ShutdownTimeout: 5 * time.Second,
	}
	if raw := os.Getenv("BOOKMARKFLOW_CHECK_WORKERS"); raw != "" {
		if n, err := strconv.Atoi(raw); err == nil && n > 0 {
			cfg.CheckWorkers = n
		}
	}
	if raw := os.Getenv("BOOKMARKFLOW_SHUTDOWN_TIMEOUT"); raw != "" {
		if d, err := time.ParseDuration(raw); err == nil && d > 0 {
			cfg.ShutdownTimeout = d
		}
	}
	return cfg
}

func envOrDefault(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
