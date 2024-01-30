set -x
set -e pipefail

#source activate py311
#eval "$(conda shell.bash hook)"
#conda activate py311
# source ~/miniconda3/bin/activate py311

cd python
python download_sogou.py
python scel2txt.py
cd ../cpp
bash go.sh
