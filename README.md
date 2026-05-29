# platform-engineering-demo
Repo to demonstrate basics of Platform engineering

docker run --name postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=employee -p 5432:5432 -d postgres

docker build -t platform-engineering-demo .

docker run -e DB_HOST="host.docker.internal" -p 8080:8080 -it platform-engineering-demo

minikube image load platform-engineering-demo:latest

kubectl apply -f kubernetes/

alias kns='kubectl config set-context --current --namespace'

kns employee

minikube service backend-service -n employee

Helm
helm install platform-demo helm/platform-engineering-demo/ \      
  -f helm/platform-engineering-demo/values-dev.yaml \
  -n employee-dev \
--create-namespace

helm install platform-demo helm/platform-engineering-demo/ \      
  -f helm/platform-engineering-demo/values-staging.yaml \
  -n employee-staging \
--create-namespace

helm install platform-demo helm/platform-engineering-demo/ \      
  -f helm/platform-engineering-demo/values-prod.yaml \
  -n employee-prod \
--create-namespace

eval $(minikube docker-env)