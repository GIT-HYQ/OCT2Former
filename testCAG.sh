 python train.py  --dataset='CAG' \
 --num_epochs=300 \
 --data_root='/home/share/clr/share/data/Coronary_mix_v4' \
 --target_root='OCTA-SS/label/segmented_images' \
 --run_dir='CAG' \
 --in_channel=1 \
 --batch_size=2 \
 --lr=5e-4 \
 --img_aug \
 --cuda_id=0 \
 --val_step=2 \
 --plot \
 --mode='test' \
 --test_run_file='2025-0817-1107_45_OCT2Former_200epoch__fold_None' \

 # --spec_interpolation \