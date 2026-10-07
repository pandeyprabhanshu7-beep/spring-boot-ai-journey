import jetbrains.buildServer.configs.kotlin.*
import jetbrains.buildServer.configs.kotlin.buildFeatures.provideAwsCredentials
import jetbrains.buildServer.configs.kotlin.buildSteps.script

version = "2025.11" // Use the version exported by your installed server.

project { buildType(AtlasAwsRelease) }

object AtlasAwsRelease : BuildType({
    name = "Atlas - trusted AWS release"
    vcs { root(DslContext.settingsRoot) }
    artifactRules = "release-image.txt"
    params {
        param("env.AWS_REGION", "us-east-1")
        param("env.AWS_ACCOUNT_ID", "111122223333")
        param("env.ECR_REPOSITORY", "atlas")
        param("env.LOCAL_IMAGE", "atlas-ci:candidate")
    }
    features {
        provideAwsCredentials { awsConnectionId = "AtlasReleaseRoleConnection" }
    }
    steps {
        script {
            name = "Build, test and publish"
            scriptContent = """
                set -eu
                python3 -m unittest discover -s code/python -p 'test_*.py'
                java code/java-core/AtlasCore.java
                docker build -t atlas-ci:candidate code/spring
                export IMAGE_TAG="%build.vcs.number%"
                bash delivery/publish_aws.sh
            """.trimIndent()
        }
    }
})
