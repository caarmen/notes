project_path=$(dirname $0)/..

pushd $project_path
./scripts/generate_doc.sh
python -m http.server -d docs -b 0.0.0.0 8811
