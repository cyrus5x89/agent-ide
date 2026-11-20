#!/bin/zsh
# chạy lần lượt từng cấp (mỗi lúc 1 job image_gen)
cd ${0:A:h}
lvs=(${@:-low medium high xhigh max ultracode}); (( $# )) || lvs=(low medium high xhigh max ultracode)
for lv in $lvs; do
  P=$(python3 -c "from prompts import *;print(BASE+' '+LEVELS['$lv'])")
  out=$(studio image stylized-concept "$P" --ref ref/clawd.png --look square 2>&1)
  f=$(print -r -- $out | python3 -c "import json,sys;print(json.load(sys.stdin)['images'][0]['file'])" 2>/dev/null)
  [[ -n $f ]] && cp "$f" "raw-$lv.png" && echo "$lv ok" || { echo "$lv FAIL"; print -r -- $out | tail -5; }
done
