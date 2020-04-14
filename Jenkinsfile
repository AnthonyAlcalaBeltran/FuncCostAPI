def bucket = 'alert-management'
def functionName = 'FuncCost'
def region = 'us-east-1'

node('slaves'){
    stage('Checkout'){
        checkout scm
    }

     stage('Test'){
    //     sh 'go get -u github.com/golang/lint/golint'
    //     sh 'go get -t ./...'
    //     sh 'golint -set_exit_status'
    //     sh 'go vet .'
    //     sh 'go test .'
    }

     stage('Build'){
    //     sh 'GOOS=linux go build -o main main.go'
        sh "ls -l"
        sh "echo '${commitID()}.zip'"
        zip zipFile:"${commitID()}.zip" , glob:''
        sh "echo 'zipeado con exito'"
    }

    stage('Push'){
        s3Upload(file:"${commitID()}.zip", bucket:"${bucket}")    
        //    aws "s3 cp '${commitID()}' s3://'${bucket}'"
    }

    stage('Deploy'){
        aws lambda update-function-code --function-name "${functionName}" \
                --s3-bucket "${bucket}" \
                --s3-key "${commitID()}.zip" \
                --region "${region}"
        //sh "aws lambda update-function-code --function-name ${functionName} \
        //        --s3-bucket ${bucket} \
        //        --s3-key ${commitID()}.zip \
        //        --region ${region}"
    }
}

def commitID() {
    sh 'git rev-parse HEAD > .git/commitID'
    def commitID = readFile('.git/commitID').trim()
    sh 'rm .git/commitID'
    commitID
}
