# sudo apt install npm
# sudo npm install -g hexo-cli
# rm -rf node_modules && npm install --force
hexo generate &&
git add source docs &&
git commit -m update &&
git push
