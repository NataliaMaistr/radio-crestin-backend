FROM --platform=linux/amd64 alpine:3.13

RUN apk add --update \
  bash \
  curl

RUN apk add rav1e-libs --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing

RUN curl -Lf# https://github.com/homebridge/ffmpeg-for-homebridge/releases/latest/download/ffmpeg-alpine-x86_64.tar.gz | tar xzf - -C / --no-same-owner

HEALTHCHECK --start-period=10s --interval=5s --timeout=3s \
  CMD  [[ ! -f /data/index.m3u8 ]] && echo "is starting.." && exit 1 || s=$(( $(date +%s) - $(stat /data/index.m3u8   -c %Y) )) && [ "$s" -lt "60" ] && echo "is up" && exit 0 || echo "is down" && rm -f /data/index.m3u8 && bash -c 'kill -s 15 -1 && (sleep 10; kill -s 9 -1)'

CMD ["ffmpeg"]
