# Resolve approved base image digests before production release.
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /work
COPY pom.xml .
COPY src src
RUN mvn -B -ntp package
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /work/target/atlas.jar /app/atlas.jar
USER 10001:10001
EXPOSE 8080
ENTRYPOINT ["java", "-XX:MaxRAMPercentage=60", "-jar", "/app/atlas.jar"]
