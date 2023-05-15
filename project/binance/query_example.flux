

// 查询tick和闪兑
from(bucket: "flash_swap")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "tick" or r["_measurement"] == "flash_swap_data")
  |> filter(fn: (r) => r["_field"] == "last" or r["_field"] == "cnvtPx")
  |> yield(name: "data_points")


