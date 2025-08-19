#!/bin/bash
# Quick PFM Compass Deployment Script
# Run with: aws-vault exec your-profile -- ./deploy.sh

set -e

echo "🚀 Quick PFM Compass Streamlit Deployment"
echo "=========================================="

# Create user-data.sh file
cat > user-data.sh << 'EOF'
#!/bin/bash
dnf update -y
dnf install -y python3 python3-pip git htop screen

sudo -u ec2-user bash << 'USEREOF'
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
pip3 install --user streamlit pandas plotly pyarrow boto3 awswrangler
mkdir -p ~/pfm-compass-app
cd ~/pfm-compass-app

# Create a basic app that will be replaced
cat > app.py << 'APPEOF'
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import boto3
import awswrangler as wr

st.title("🎯 PFM Compass - Retirement Planning")
st.write("App is initializing... Loading data from S3...")

try:
    s3_path = "s3://jp-data-lake-experimental-production/lakehouse_experimental_jp_production/pfm_compass_retirement_predictions_internal_v1/"
    df = wr.s3.read_parquet(path=s3_path, dataset=True)
    st.success(f"✅ Loaded {len(df):,} retirement scenarios from S3!")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"S3 connection error: {e}")
    st.info("Upload your full app.py to complete setup.")
APPEOF

USEREOF

# Start Streamlit in background
sudo -u ec2-user bash << 'STARTEOF'
cd /home/ec2-user/pfm-compass-app
source ~/.bashrc
nohup /home/ec2-user/.local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
STARTEOF

echo "Streamlit setup completed" >> /var/log/user-data.log
EOF

# Variables
REGION="ap-northeast-1"
INSTANCE_NAME="pfm-compass-streamlit"
KEY_NAME="pfm-compass-key-$(date +%s)"

echo "📋 Region: $REGION"
echo "📋 Instance: $INSTANCE_NAME"
echo "📋 Key: $KEY_NAME"
echo ""

# Get your current IP
MY_IP=$(curl -s ifconfig.me)/32
echo "🔒 Your IP: $MY_IP"

# Create key pair
echo "🔑 Creating key pair..."
aws ec2 create-key-pair \
    --key-name $KEY_NAME \
    --query 'KeyMaterial' \
    --output text \
    --region $REGION > ${KEY_NAME}.pem
chmod 400 ${KEY_NAME}.pem
echo "✅ Key saved: ${KEY_NAME}.pem"

# Get default VPC
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text --region $REGION)
echo "🌐 Using VPC: $VPC_ID"

# Create security group
SG_NAME="pfm-compass-sg-$(date +%s)"
echo "🛡️ Creating security group: $SG_NAME"

SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name $SG_NAME \
    --description "PFM Compass Streamlit Security Group" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text \
    --region $REGION)

# Add rules
echo "🔓 Adding security rules..."
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 22 \
    --cidr $MY_IP \
    --region $REGION

aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 8501 \
    --cidr $MY_IP \
    --region $REGION

echo "✅ Security group created: $SECURITY_GROUP_ID"

# Launch instance
echo "🚀 Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0d52744d6551d851e \
    --count 1 \
    --instance-type t3.micro \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --user-data file://user-data.sh \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --region $REGION \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ Instance launched: $INSTANCE_ID"

# Wait for running state
echo "⏳ Waiting for instance to start..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text \
    --region $REGION)

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "========================"
echo ""
echo "📊 Your PFM Compass app will be available at:"
echo "   🔗 http://$PUBLIC_IP:8501"
echo ""
echo "⏳ Please wait 2-3 minutes for the app to fully initialize"
echo ""
echo "🔧 Instance details:"
echo "   📍 Instance ID: $INSTANCE_ID"
echo "   🌐 Public IP: $PUBLIC_IP"
echo "   🔑 SSH Key: ${KEY_NAME}.pem"
echo ""
echo "🖥️ To connect via SSH:"
echo "   ssh -i ${KEY_NAME}.pem ec2-user@$PUBLIC_IP"
echo ""
echo "📁 To upload your full app:"
echo "   scp -i ${KEY_NAME}.pem app.py ec2-user@$PUBLIC_IP:~/pfm-compass-app/app.py"
echo ""
echo "🔄 To restart the app after uploading:"
echo "   ssh -i ${KEY_NAME}.pem ec2-user@$PUBLIC_IP 'cd ~/pfm-compass-app && pkill streamlit && nohup ~/.local/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &'"
echo ""

# Clean up temp files
rm -f user-data.sh

echo "🚀 Ready to go! Check your app at: http://$PUBLIC_IP:8501"