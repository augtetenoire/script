
declare -a conf=(
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_mixed_alldata_sets_test_set.xyz"
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_Ru55_test_set.xyz"
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_Ru114_test_set.xyz"
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_Ru256_test_set.xyz"
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_Ru288_test_set.xyz"
"/scratch-store/scratch/tetenoir/julien_lam/mace_data/data_created_bis/macefile_Ru576_test_set.xyz"
                )


for file in "${conf[@]}" ; do

base=$(basename ${file})
name=mace_eval_${base}

echo "Evaluating: $file"

python3 /share/lcbcsrv9/lcbcdata/tetenoir/github/mace/mace/cli/eval_configs.py \
    --configs=${file} \
    --model='../mace_foundation_MPA_0_retrain_multihead_stagetwo.model' \
    --output=${name} \
    --head='Default' \
    --batch_size=10 \
    --default_dtype='float64' \
    --device='cuda' \

echo "Created file:  $name"

temp=${base/.xyz/.pdf}
pdfname=${temp/macefile_/}

python3 /share/lcbcsrv9/lcbcdata/tetenoir/github/script/mace_eval_plot.py ${name} ${pdfname}

done
