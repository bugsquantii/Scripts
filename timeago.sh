#!/bin/bash

calculate_days_since() {
  local input_date="$1"
  local target_timestamp=$(date -d "$input_date" +%s)
  local current_timestamp=$(date +%s)
  local seconds_diff=$((current_timestamp - target_timestamp))
  local days_diff=$((seconds_diff / 86400))
  echo "$days_diff"
}

input_date="$1" #Format: "YYYY-MM-DD"
days_since=$(calculate_days_since "$input_date")

echo "$days_since days"
