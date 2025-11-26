#!/bin/sh
PROJECT_ROOT=$(realpath $(dirname $0))
BIN_DIR=${BIN_DIR:-"$HOME/.local/bin"}
CONFIG_DIR=${CONFIG_DIR:-"$HOME/.config/rclone_tasks"}
SYSTEMD_USER_DIR=${SYSTEMD_USER_DIR:-"$HOME/.config/systemd/user"}
RCLONE_CONFIG_CRYPT=${RCLONE_CONFIG_CRYPT:-"yes"}

sed -i "s|@INSTALL_DIR|${BIN_DIR}|g" rclone.service
sed -i "s|@CONFIG_DIR|${CONFIG_DIR}|g" rclone.service

if [ ! -d "${BIN_DIR}" ];then
    mkdir -p "${BIN_DIR}"
fi

if [ ! -d "${CONFIG_DIR}" ];then
    mkdir -p "${CONFIG_DIR}"
fi

case $RCLONE_CONFIG_CRYPT in
    1|yes|Yes|sim|Sim) SERVICE_FILE="$PROJECT_ROOT/service_templates/rclone.service_w_env";;
    *) SERVICE_FILE="$PROJECT_ROOT/service_templates/rclone.service_wo_env";;
esac

cp "$PROJECT_ROOT/rclone_tasks.py" "$INSTALL_DIR/rclone_tasks"
cp "$PROJECT_ROOT/rclone_tasks.json" "$CONFIG_DIR/rclone_tasks.json"
cp "$SERVICE_FILE" "$SYSTEMD_USER_DIR/rclone.service"

chmod +x "$INSTALL_DIR/rclone_tasks"

systemctl --user daemon-reload
systemctl --user enable --now rclone.service
