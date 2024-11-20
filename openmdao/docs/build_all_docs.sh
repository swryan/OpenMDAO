#!/bin/bash
echo "NOTE: if 'Bad config' error occurs during ipcluster startup, try deleting the $HOME/.ipython/profile_mpi directory"
rm -rf openmdao_book/_srcdocs openmdao_book/_build
export OLD_OPENMDAO_REPORTS=${OPENMDAO_REPORTS}
export OPENMDAO_REPORTS=0

python build_source_docs.py;

JB_VER=`jupyter-book --version`
if [[ $JB_VER == v2* ]]; then
    echo "jupyter-book version 2.x detected ($JB_VER)..."
    cd openmdao_book
    jupyter-book build --html || export OPENMDAO_REPORTS=${OLD_OPENMDAO_REPORTS}
    cd ..
    pip install sphinx_book_theme
    python copy_build_artifacts.py
else
    echo "jupyter-book version 1.x detected ($JB_VER)..."
    jupyter-book build  --html openmdao_book/ || export OPENMDAO_REPORTS=${OLD_OPENMDAO_REPORTS}
    python copy_build_artifacts.py
fi
