for diagram in ./*.puml
do 
  docker run -u $(id -u):$(id -g) --rm -v $(pwd):/data -it hrektts/plantuml plantuml ${diagram}
done
