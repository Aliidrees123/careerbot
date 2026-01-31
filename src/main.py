from dotenv import load_dotenv
import os
import json
import requests
from openai import OpenAI
from anthropic import Anthropic
from pypdf import PdfReader
import gradio as gr
from rich.console import Console

console = Console()

load_dotenv()
