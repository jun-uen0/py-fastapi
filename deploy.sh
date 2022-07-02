#!/bin/sh

aws_region="ap-northeast-1"
aws_account_id="311575258506"
aws_ecr_name="py-fastapi"

# aws_cluster_name="changeme"
# aws_service_name="changeme"

ecr_image_tag="prod"

# ECR Login
echo "Login to ECR.."
echo "You need to login to AWS profile attated ECR access policy..."
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $aws_account_id.dkr.ecr.$aws_region.amazonaws.com

# Build Image with linux/amd64 (To avoid building with arm64)
echo "Building image..."
docker build -f server/Dockerfile --platform=linux/amd64 -t $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:$ecr_image_tag ./server/

# Push to ECR
echo "Pushing image to AWS ECR..."
docker push $aws_account_id.dkr.ecr.$aws_region.amazonaws.com/$aws_ecr_name:$ecr_image_tag

# Update ECS Service (Optional)
# echo "updating ECS service..."
# aws ecs update-service --cluster $aws_cluster_name --service $aws_service_name --force-new-deployment

echo "Done!"