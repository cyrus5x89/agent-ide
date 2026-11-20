#!/bin/zsh
# giữ nguyên thân của ảnh mẫu, chỉ đổi tóc + hiệu ứng (studio image identity-preserve)
#   medium ← thân gầy cơ (ref/body-lean.png) · high, xhigh, ultracode ← thân của max (ref/body-max.png)
cd ${0:A:h}
KEEP="Keep the creature's body EXACTLY as in Image 1: same orange square body, same muscles, arms, legs, eyes, black outline, size and position. Change ONLY the hair and the effects described here. Keep the plain flat #0E0E0E background and the same anime cel-shaded style."
typeset -A SRC DO
SRC=(medium ref/body-lean.png high ref/body-max.png xhigh ref/body-max.png ultracode ref/body-max.png)
DO=(
 medium "Hair: sharper spiky hair in a DEEP DARK GOLD, short-medium length. Effects: remove all flames and embers; only a thin golden outline glow hugging the body and 2-3 tiny blue-white electric sparks near the hair."
 high "Hair: very LONG golden-yellow spiky mane flowing down behind the body almost to the ground, no eyebrows. Effects: remove the blue flame aura and sparkles; only a thin golden outline glow and 4-5 small yellow electric sparks. Restrained, the long hair is the star."
 xhigh "Hair: SHORT spiky hair in CRIMSON RED. Effects: replace the blue aura with a soft red-orange divine flame aura and a few red embers floating."
 ultracode "Hair: SHORT spiky SILVER-WHITE hair; eyes glow silver-white. Effects: replace the blue aura with a tall silvery-white and pale blue flame aura with floating light particles, calm and god-like, the most radiant of all."
)
lvs=($@); (( $# )) || lvs=(medium high xhigh ultracode)
for lv in $lvs; do
  out=$(studio image identity-preserve "$KEEP $DO[$lv]" --ref $SRC[$lv] --name "$lv-$(date +%s)" 2>&1)
  f=$(print -r -- $out | python3 -c "import json,sys;print(json.load(sys.stdin)['images'][0]['file'])" 2>/dev/null)
  [[ -n $f ]] && cp "$f" "raw-$lv.png" && echo "$lv ok" || { echo "$lv FAIL"; print -r -- $out | grep -A2 '"msg"'; }
done
