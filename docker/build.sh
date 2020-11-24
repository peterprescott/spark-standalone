# -- Get Builder's Username

source ../.env

# -- Software Stack Version

SPARK_VERSION="3.0.0"
HADOOP_VERSION="2.7"
JUPYTERLAB_VERSION="2.1.5"

# -- Building the Images

docker build \
  -f ./cluster_base.Dockerfile \
  -t ${BUILDER}/cluster-base .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg hadoop_version="${HADOOP_VERSION}" \
  -f ./spark-base.Dockerfile \
  -t ${BUILDER}/spark-base .

docker build \
  -f ./spark-master.Dockerfile \
  -t ${BUILDER}/spark-master .

docker build \
  -f ./spark-worker.Dockerfile \
  -t ${BUILDER}/spark-worker .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
  -f ./jupyterlab.Dockerfile \
  -t ${BUILDER}/jupyterlab .


docker push ${BUILDER}/cluster-base
docker push ${BUILDER}/spark-base
docker push ${BUILDER}/spark-master
docker push ${BUILDER}/spark-worker
docker push ${BUILDER}/jupyterlab
