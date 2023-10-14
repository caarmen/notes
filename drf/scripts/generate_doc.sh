project_path=$(dirname $0)/../notes/

pushd $project_path
python -m manage spectacular  --format openapi-json > ../docs/openapi.json
