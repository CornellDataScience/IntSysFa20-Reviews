# IntSysFa20-Reviews

This will be our repository for doing code reviews. Remember, this is the current plan:  

- Each project has its own branch (`fairmandering`, `mci` and `kde`). 
- Each branch has a pull request associated with it. Do NOT commit anything to the `main` branch and please do not merge any pull requests.
- Each project should add the files that you want to be reviewed to your project's branch. This can be done in two ways: 
    - If everyone on the group has been working on overlapping files, just add those files to the branch.
    - If you think it will be cleaner to separate your code from your team members' code, create a folder per person on your team (eg: `magd` and `katie`) and dump your files in that folder.
- Once you are done adding your files that you want to be reviewed, notify the leads (Cora and Samar) and the leads will assign reviewers to your pull request. 

Reviewers, once you have been assigned to a pull request, please do the following while going through the pull request:
- If you find any functions/classes undocumented, please add a comment requesting that the project group add some documentation `Documentation suggestion:`
- If you find some code that is obfuscating or very dense, add a comment suggesting that the authors break the code into functions/subcomponents, prefacing it with `Structure suggestion:`. It would be better if you could specify exactly how the authors can make the code less confusing (eg: if one file contains the training script, model architecture and experiments, suggest that the model architecture be defined in a separate file/folder, the training script be as invariant as possible to differences in model architecture, and that experiments be performed in as modular a manner as possible, using the training/model components already created. Remember the good ol' programming principles from CS 2110 and CS 3110!)
- If you have a suggestion for the implementation of a function (either to improve efficiency or correctness), please mention this by prefacing your comment with `Implementation suggestion:`

I think these categories should be broad enough for our purposes. If you think there's something I am missing, don't hesitate to reach out to me or Cora over Slack!
