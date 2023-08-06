

python setup.py sdist bdist_wheel


twine check dist/*


# 上传到测试环境
twine upload --repository testpypi dist/*

# 上传到正式环境
twine upload dist/*


pip install -i https://test.pypi.org/simple/ dbartist==0.0.5