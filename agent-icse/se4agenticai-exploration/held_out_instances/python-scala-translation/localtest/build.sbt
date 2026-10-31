// Build configuration for the RecordBatch held-out instance project
// (same toolchain/deps as the original scala_tokenizer/build.sbt, unused
// circe deps kept for parity rather than pruning to minimize drift)

ThisBuild / scalaVersion := "2.13.12"
ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / organization := "com.example"

lazy val root = (project in file("."))
  .settings(
    name := "scala-recordbatch",
    libraryDependencies ++= Seq(
      "io.circe" %% "circe-core" % "0.14.6",
      "io.circe" %% "circe-generic" % "0.14.6",
      "io.circe" %% "circe-parser" % "0.14.6",

      "org.scalatest" %% "scalatest" % "3.2.17" % Test,
      "org.scalatestplus" %% "scalacheck-1-17" % "3.2.17.0" % Test
    ),

    scalacOptions ++= Seq(
      "-deprecation",
      "-feature",
      "-unchecked",
      "-Xlint:infer-any",
      "-Xlint:missing-interpolator"
    )
  )
