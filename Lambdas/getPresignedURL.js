// This is the function you will need in your Lambda to make the backend work.
// Follow along in the tutorial to see how to set this up.
const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.REGION || 'us-east-1' })
const s3 = new AWS.S3();

const uploadBucket = 'audios-bbva'

exports.handler = async (event) => {
  const result = await getUploadURL(event.body.split('"')[3])
  console.log('evento: ',event)
  console.log('Result: ', result)
  return result
};

const getUploadURL = async function(name) {
  console.log('getUploadURL started')
  let actionId = name.replace(/\s+/g, '_')

  var s3Params = {
    Bucket: uploadBucket,
    Key:  `${actionId}`,
    ContentType: 'audio/wav',
    CacheControl: 'max-age=31104000',
    ACL: 'public-read',
  };

  return new Promise((resolve, reject) => {
    // Get signed URL
    let uploadURL = s3.getSignedUrl('putObject', s3Params)
    resolve({
      "statusCode": 200,
      "isBase64Encoded": false,
      "headers": {
        "Access-Control-Allow-Origin": "*"
      },
      "body": JSON.stringify({
          "uploadURL": uploadURL,
          "photoFilename": `${actionId}`
      })
    })
  })
}
