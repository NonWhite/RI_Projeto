counter=0

for i in $(ls ../raw_data/*.sgm)
do
	python splitter.py $i $((counter*1000))
	counter=$((counter+1))
done 
