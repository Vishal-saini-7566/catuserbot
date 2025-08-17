
FROM catub/core:bullseye

# Working directory
WORKDIR /userbot

# Timezone
ENV TZ=Asia/Kolkata

## Copy files into the Docker image
COPY . .

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
