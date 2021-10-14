to push from pc to source repo: 
git remote add google ssh://rashi1999agarwal@gmail.com@source.developers.google.com:2022/p/gcp-free-trial-experiment/r/gcp-experiments

git push --all google

======================================
Clone this repo to local git repository

git clone ssh://rashi1999agarwal@gmail.com@source.developers.google.com:2022/p/gcp-free-trial-experiment/r/gcp-experiments

cd gcp-experiments

After you have commited your code push to git repo
git push -u origin master

========================================

 Setup SSH key. Learn how

If you already have a SSH key on your machine, skip to step 2. Find SSH Keys on your machine .
Register the SSH key with Google Cloud.
Clone this repository to a local Git repository:

    Clone with command line
    $ git clone ssh://rashi1999agarwal@gmail.com@source.developers.google.com:2022/p/gcp-free-trial-experiment/r/gcp-experiments

    Or clone with VS Code Clone 

Note: This may display the following message that is safe to ignore:
"warning: You appear to have cloned an empty repository."
Switch to your new local Git repository:
$ cd gcp-experiments
After you've committed code to your local Git repository, push it to this repository:
$ git push -u origin master
Once you've completed all these steps, refresh your browser. 

===================================

 Setup SSH key. Learn how

If you already have a SSH key on your machine, skip to step 2. Find SSH Keys on your machine .
Register the SSH key with Google Cloud.
Add your Cloud Repository as a remote:
$ git remote add google ssh://rashi1999agarwal@gmail.com@source.developers.google.com:2022/p/gcp-free-trial-experiment/r/gcp-experiments
Push from your local Git repository:
$ git push --all google
Once you've completed all these steps, refresh your browser. 

===============================================

 Install the Google Cloud SDK .
Provide your authentication credentials:
$ gcloud init
Clone this repository to a local Git repository:
$ gcloud source repos clone gcp-experiments --project=gcp-free-trial-experiment
Note: This may display the following message that is safe to ignore:
"Warning: remote HEAD refers to a nonexistent ref, unable to checkout."
Switch to your new local Git repository:
$ cd gcp-experiments
After you've committed code to your local Git repository, push it to this repository:
$ git push -u origin master
Once you've completed all these steps, refresh your browser. 

=====================================

 Generate and store your Git credentials.
Add your Cloud Repository as a remote:
$ git remote add google https://source.developers.google.com/p/gcp-free-trial-experiment/r/gcp-experiments
Push from your local Git repository:
$ git push --all google
Once you've completed all these steps, refresh your browser. 