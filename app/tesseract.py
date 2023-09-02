import functools
from flask import Flask, Blueprint, render_template, request, jsonify
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import sys
import re
import json

from filemgmnt import upload_file, request_data_type

bp = Blueprint('tesseract', __name__, url_prefix='/api')

bp.psm = '3'
bp.oem = '3'

def ocr_core(filepath):
  """
  This function will handle the core OCR processing of images.
  """
  image = Image.open(filepath)
  custom_oem_psm_config = '--oem ' + bp.oem + ' --psm ' + bp.psm
  text = pytesseract.image_to_string(image, config=custom_oem_psm_config) 
  return text

@bp.route('/ocr', methods = ['POST'])
def ocr():
  """
  This function will handle the upload a file and return of the extracted text via tesseract.
  No spacy or other processing will be done.
  """
  if request.method == 'POST':

    psm = request.form.get("psm")
    if psm is not None:
      bp.psm = json.loads(psm)

    oem = request.form.get("oem")
    if oem is not None:
      bp.oem = json.loads(oem)

    filepaths = upload_file(request)

    if filepaths is None:
      return jsonify(error='No file provided with key of "file" found')
    else:
      if len(filepaths) == 1:
        extracted_text = ocr_core(filepaths[0])
        lines = re.split('\n\n|\n',extracted_text)
        return jsonify(text=extracted_text, lines=lines)
      else:
        extracted_text = ""
        for filepath in filepaths:
          extracted_text += ocr_core(filepath)
        lines = re.split('\n\n|\n',extracted_text)
        return jsonify(text=extracted_text, lines=lines)
