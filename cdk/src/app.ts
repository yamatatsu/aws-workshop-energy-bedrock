import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3Deployment from 'aws-cdk-lib/aws-s3-deployment';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'WorkshopEnergyBedrock', {
  env: {
    region: 'us-east-1',
  }
});

const bucket = new s3.Bucket(stack, 'SensorData', {
  blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
  encryption: s3.BucketEncryption.S3_MANAGED,
  autoDeleteObjects: true,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
})

new s3Deployment.BucketDeployment(stack, 'DeploySensorData', {
  sources: [s3Deployment.Source.asset('./assets')],
  destinationBucket: bucket,
  retainOnDelete: false,
});