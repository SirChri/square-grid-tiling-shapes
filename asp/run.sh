clingo ./main.lp ./input1.lp --parallel 10 --opt-strategy=bb,lin --quiet=1 --out-hide-aux --outf=2 --time-limit=300 --warn none | python3 format-out.py > ./out/main.html
