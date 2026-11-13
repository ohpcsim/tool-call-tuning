GTO registers an artifact version with an annotated Git tag such as `todo-model@v0.0.1`, which points to the version commit.
It assigns a stage with a second annotated tag such as `todo-model#experiment#1`; a tag such as `desk-model#rejected!#5` records a stage unassignment.
The `artifacts:` block in `studies/todo/dvc.yaml` declares the to-do artifacts and their paths; this excerpt does not declare the desk artifact.
`versions.txt` contains tag names, target commits and tagger dates only; it excludes annotation messages.
