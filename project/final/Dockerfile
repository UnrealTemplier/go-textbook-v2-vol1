# syntax=docker/dockerfile:1

# Этап 1: сборка статического бинарника Go 1.24
FROM golang:1.24-alpine AS builder

WORKDIR /src
COPY go.mod ./
COPY final ./final

RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/bookmarkflow ./final/cmd/bookmarkflow

# Этап 2: минимальный образ без компилятора и оболочки
FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /app
COPY --from=builder /out/bookmarkflow /app/bookmarkflow

ENV BOOKMARKFLOW_ADDR=":8080" \
    BOOKMARKFLOW_DATA_FILE="/data/bookmarks.json" \
    BOOKMARKFLOW_CHECK_WORKERS="4"

EXPOSE 8080
USER nonroot:nonroot

ENTRYPOINT ["/app/bookmarkflow"]
