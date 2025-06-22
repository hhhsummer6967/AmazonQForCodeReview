#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import requests
import os
import sys
import json
import datetime
import asyncio
import aiohttp
from pathlib import Path
import re                                


# GitLab API configuration
gitlab_url = os.environ.get("CI_SERVER_URL", "")
project_id = os.environ.get("CI_PROJECT_ID", "")
mr_iid = os.environ.get("CI_MERGE_REQUEST_IID", "")
private_token = os.environ.get("REGISTRATION_TOKEN", "")
pipeline_id = os.environ.get("CI_PIPELINE_ID", "")
commit_sha = os.environ.get("CI_COMMIT_SHA", "")
project_namespace = os.environ.get("CI_PROJECT_NAMESPACE", "")
project_name = os.environ.get("CI_PROJECT_NAME", "")
username = "AmazonQ"



# File paths
review_file_path = "amazon_q_review.md"
"""if pipeline_id:
    if mr_iid:
        review_file_path = f"amazon_q_review_{pipeline_id}.md"
    else:
        review_file_path = f"amazon_q_full_review_{pipeline_id}.md"
"""
# Constants
LARGE_REPORT_THRESHOLD_MB = 1
CHUNK_SIZE = 500000  # ~500KB per chunk

def read_review_content():
    """Read the review content from the file"""
    try:
        with open(review_file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read review file: {e}")
        sys.exit(1)

def add_mr_comment(content):
    """Add a comment to a merge request"""
    if not all([gitlab_url, project_id, mr_iid, private_token]):
        print("Missing required environment variables for MR comment")
        sys.exit(1)
        
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }

    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    response = requests.post(url, headers=headers, json={"body": content})

    if response.status_code >= 200 and response.status_code < 300:
        print(f"Successfully added comment: {response.status_code}")
        print(response.json())
        return True
    else:
        print(f"Failed to add comment: {response.status_code}")
        print(response.text)
        return False

async def add_mr_comment_async(content):
    """Add a comment to a merge request asynchronously"""
    if not all([gitlab_url, project_id, mr_iid, private_token]):
        print([gitlab_url, project_id, mr_iid, private_token])
        print("Missing required environment variables for MR comment")
        return False
        
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }

    url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json={"body": content}) as response:
                if response.status >= 200 and response.status < 300:
                    print(f"Successfully added comment: {response.status}")
                    return True
                else:
                    print(f"Failed to add comment: {response.status}")
                    text = await response.text()
                    print(text)
                    return False
        except Exception as e:
            print(f"Exception during comment creation: {e}")
            return False

def create_wiki_page(title, content):
    """Create a wiki page in the GitLab repository"""
    if not all([gitlab_url, project_id, private_token]):
        print("Missing required environment variables for wiki creation")
        sys.exit(1)
        
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }

    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis"
    data = {
        "title": title,
        "content": content
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("2222")
    print(response.text)
    
    if response.status_code == 201:
        wiki_slug = title.lower().replace(" ", "-")
        wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"
        print(f"Wiki page '{title}' created successfully! URL: {wiki_url}")
        return True
    elif response.status_code == 400:  # Page already exists
        # Try to update the page instead
        try:
            response_json = response.json()
            if "message" in response_json and "base" in response_json["message"]:
                error_msg = response_json["message"]["base"][0]
                if "Duplicate page" in error_msg:
                    # Extract existing file name from error message
                    match = re.search(r'file (.*?)\.md', error_msg)
                    if match:
                        existing_file = match.group(1)
                        return update_wiki_page(existing_file, title, content)
                else:
                    print(f"Bad request error: {error_msg}")
                    sys.exit(1)
        except:
            pass
        # Fallback to default slug if error parsing fails
        slug = title.lower().replace(" ", "-")
        return update_wiki_page(slug, title, content)
    else:
        print(f"Failed to create wiki page: {response.status_code}")
        print(response.text)
        return False

async def create_wiki_page_async(title, content):
    """Create a wiki page asynchronously"""
    if not all([gitlab_url, project_id, private_token]):
        print("Missing required environment variables for wiki creation")
        return False
    
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis"
    data = {
        "title": title,
        "content": content
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=data) as response:
                print("11111")
                print(response.text)
                print(response.status)
                if response.status == 201:
                    wiki_slug = title.lower().replace(" ", "-")
                    wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"                    
                    print(f"Wiki URL: {wiki_url}")
                    return True
                elif response.status == 400:  # Page already exists
                    # Try to update the page instead
                    print(3333)
                    try:
                        response_json = await response.json()
                        if "message" in response_json and "base" in response_json["message"]:
                            error_msg = response_json["message"]["base"][0]
                            if "Duplicate page" in error_msg:
                                print(4444)

                                # Extract existing file name from error message
                                match = re.search(r'file (.*?)\.md', error_msg)
                                if match:
                                    existing_file = match.group(1)
                                    return await update_wiki_page_async(existing_file, title, content)
                            else:
                                print(f"Bad request error: {error_msg}")
                                sys.exit(1)
                    except:
                        pass
                    # Fallback to default slug if error parsing fails
                    slug = title.lower().replace(" ", "-")
                    return await update_wiki_page_async(slug, title, content)
                else:
                    print(f"Failed to create wiki page: {response.status}")
                    text = await response.text()
                    print(text)
                    return False
        except Exception as e:
            print(f"Exception during wiki page creation: {e}")
            return False

def update_wiki_page(slug, title, content):
    """Update an existing wiki page"""
    if not all([gitlab_url, project_id, private_token]):
        print("Missing required environment variables for wiki update")
        sys.exit(1)
        
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis/{slug}"
    data = {
        "title": title,
        "content": content
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        wiki_slug = title.lower().replace(" ", "-")
        wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"
        print(f"Wiki page '{title}' updated successfully! URL: {wiki_url}")
        return True
    else:
        print(f"Failed to update wiki page: {response.status_code}")
        print(response.text)
        return False

async def update_wiki_page_async(slug, title, content):
    """Update a wiki page asynchronously"""
    if not all([gitlab_url, project_id, private_token]):
        print("Missing required environment variables for wiki update")
        return False
    
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis/{slug}"
    data = {
        "title": title,
        "content": content
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(url, headers=headers, json=data) as response:
                print("55555")
                print(response.status)
                print(response.text)
                print(url)
                if response.status == 200:
                    wiki_slug = title.lower().replace(" ", "-")
                    wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"
                    print(f"Wiki page '{title}' updated successfully!")
                    print(f"Wiki URL: {wiki_url}")
                    return True
                else:
                    print(f"Failed to update wiki page: {response.status}")
                    text = await response.text()
                    print(text)
                    return False
        except Exception as e:
            print(f"Exception during wiki page update: {e}")
            return False

async def get_wiki_page_content(slug):
    """Get wiki page content asynchronously"""
    if not all([gitlab_url, project_id, private_token]):
        print("Missing required environment variables")
        return None
    
    headers = {
        "PRIVATE-TOKEN": private_token
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis/{slug}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("content", "")
                else:
                    print(f"Failed to get wiki page: {response.status}")
                    return None
        except Exception as e:
            print(f"Exception during wiki page retrieval: {e}")
            return None

def update_wiki_index(new_report_title, new_report_slug):
    """Update or create the wiki index page with links to all reports"""
    index_title = "Code Review Reports Index"
    index_slug = "code-review-reports-index"
    
    # Try to get existing index
    headers = {
        "PRIVATE-TOKEN": private_token,
        "Content-Type": "application/json"
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis/{index_slug}"
    response = requests.get(url, headers=headers)
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if response.status_code == 200:
        # Index exists, update it
        existing_content = response.json().get("content", "")
        
        # Add new report to the table if it doesn't already exist
        if new_report_title not in existing_content:
            # Check if the table exists
            if "| Report | Date | Type |" in existing_content:
                # Add to existing table
                table_entry = f"| [{new_report_title}]({new_report_slug}) | {current_date} | {'MR Review' if mr_iid else 'Full Review'} |\n"
                # Insert the new entry after the table header and separator
                lines = existing_content.split('\n')
                table_start_idx = -1
                for i, line in enumerate(lines):
                    if "| Report | Date | Type |" in line:
                        table_start_idx = i
                        break
                
                if table_start_idx >= 0:
                    lines.insert(table_start_idx + 2, table_entry)
                    updated_content = '\n'.join(lines)
                else:
                    # Shouldn't happen, but just in case
                    updated_content = existing_content + "\n" + table_entry
            else:
                # Create new table
                table_header = "\n\n| Report | Date | Type |\n|--------|------|------|\n"
                table_entry = f"| [{new_report_title}]({new_report_slug}) | {current_date} | {'MR Review' if mr_iid else 'Full Review'} |\n"
                updated_content = existing_content + table_header + table_entry
                
            return update_wiki_page(index_slug, index_title, updated_content)
    else:
        # Create new index
        content = f"""# Code Review Reports Index

This page contains links to all code review reports generated for the project.

| Report | Date | Type |
|--------|------|------|
| [{new_report_title}]({new_report_slug}) | {current_date} | {'MR Review' if mr_iid else 'Full Review'} |
"""
        return create_wiki_page(index_title, content)
    
    return True

async def update_wiki_index_async(new_report_title, new_report_slug):
    """Update or create the wiki index page with links to all reports asynchronously"""
    index_title = "Code Review Reports Index"
    index_slug = "code-review-reports-index"
    
    # Try to get existing index
    headers = {
        "PRIVATE-TOKEN": private_token
    }
    
    url = f"{gitlab_url}/api/v4/projects/{project_id}/wikis/{index_slug}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                report_type = 'MR Review' if mr_iid else 'Full Review'
                
                if response.status == 200:
                    # Index exists, update it
                    data = await response.json()
                    existing_content = data.get("content", "")
                    
                    # Add new report to the table if it doesn't already exist
                    if new_report_title not in existing_content:
                        table_entry = f"| [{new_report_title}]({new_report_slug}) | {current_date} | {report_type} |\n"
                        
                        if "| Report | Date | Type |" in existing_content:
                            # Add to existing table - simplified logic
                            lines = existing_content.split('\n')
                            table_header_idx = next((i for i, line in enumerate(lines) 
                                                if "| Report | Date | Type |" in line), -1)
                            
                            if table_header_idx >= 0:
                                lines.insert(table_header_idx + 2, table_entry)
                                updated_content = '\n'.join(lines)
                            else:
                                updated_content = existing_content + "\n" + table_entry
                        else:
                            # Create new table
                            table_header = "\n\n| Report | Date | Type |\n|--------|------|------|\n"
                            updated_content = existing_content + table_header + table_entry
                            
                        return await update_wiki_page_async(index_slug, index_title, updated_content)
                else:
                    # Create new index
                    content = f"""# Code Review Reports Index

This page contains links to all code review reports generated for the project.

| Report | Date | Type |
|--------|------|------|
| [{new_report_title}]({new_report_slug}) | {current_date} | {report_type} |
"""
                    return await create_wiki_page_async(index_title, content)
        except Exception as e:
            print(f"Exception during wiki index update: {e}")
            return False
    
    return True

def generate_report_title():
    """Generate a title for the report based on the context"""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if mr_iid:
        return f"{current_date}-MR Review #{mr_iid}"
    else:
        return f"{current_date}-基础全库审核-PipelineID-{pipeline_id}"

async def retry_async(func, *args, max_attempts=3, **kwargs):
    """Retry an async function with exponential backoff"""
    attempt = 0
    while attempt < max_attempts:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            if attempt == max_attempts:
                print(f"Failed after {max_attempts} attempts: {e}")
                return None
            
            wait_time = 2 ** attempt  # 指数退避
            print(f"Attempt {attempt} failed, retrying in {wait_time}s: {e}")
            await asyncio.sleep(wait_time)

async def upload_large_report(title, content):
    """Upload large report content in chunks"""
    # 1. 创建初始页面
    print(f"Creating initial wiki page: {title}")
    initial_content = f"# {title}\n\n*Content is being uploaded in chunks...*"
    success = await create_wiki_page_async(title, initial_content)
    if not success:
        return False
    
    # 2. 计算分块
    content_chunks = [content[i:i+CHUNK_SIZE] 
                     for i in range(0, len(content), CHUNK_SIZE)]
    total_chunks = len(content_chunks)
    
    print(f"Report will be uploaded in {total_chunks} chunks")
    
    # 3. 生成slug
    slug = title.lower().replace(" ", "-")
    
    # 4. 逐块上传
    for i, chunk in enumerate(content_chunks):
        if i == 0:
            # 第一块替换初始内容
            success = await update_wiki_page_async(slug, title, chunk)
        else:
            # 后续块追加到页面
            current_content = await get_wiki_page_content(slug)
            if current_content is None:
                print(f"Failed to get current content for chunk {i+1}/{total_chunks}")
                return False
            
            updated_content = current_content + chunk
            success = await update_wiki_page_async(slug, title, updated_content)
        
        if not success:
            print(f"Failed to upload chunk {i+1}/{total_chunks}")
            return False
        
        print(f"Uploaded chunk {i+1}/{total_chunks} ({(i+1)/total_chunks*100:.1f}%)")
    
    # 输出最终的Wiki URL
    wiki_slug = title.lower().replace(" ", "-")
    wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"
    print(f"Successfully uploaded large report: {title}")
    print(f"Final Wiki URL: {wiki_url}")
    return True

async def async_main():
    # Read the review content
    review_content = read_review_content()
    
    # Add metadata to the content
    metadata = f"""
---
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Pipeline ID: {pipeline_id}
Commit: {commit_sha}
Reviewer: {username}
---

"""
    enhanced_content = metadata + review_content
    
    # Check if this is a large report
    content_size_mb = len(enhanced_content) / (1024 * 1024)
    large_report = content_size_mb > LARGE_REPORT_THRESHOLD_MB
    
    # Determine if this is an MR review or a manual review
    if mr_iid:
        # MR Review - Always add comment to MR, regardless of size
        print(f"Adding comment to Merge Request #{mr_iid}")
        
        if large_report:
            print(f"Large report detected ({content_size_mb:.2f}MB), but still adding directly to MR comment")
            
        # Add comment to MR
        success = await add_mr_comment_async(enhanced_content)
        
        if success:
            print(f"Successfully added review comment to MR #{mr_iid}")
    else:
        # Full repository review - Create Wiki page
        report_title = generate_report_title()
        report_slug = report_title.lower().replace(" ", "-")
        wiki_slug = report_title.lower().replace(" ", "-")
        wiki_url = f"{gitlab_url}/{project_namespace}/{project_name}/-/wikis/{wiki_slug}"
        
        print(f"Creating wiki page for full repository review: {report_title}")
        
        if large_report:
            print(f"Large report detected ({content_size_mb:.2f}MB), using chunked upload")
            success = await upload_large_report(report_title, enhanced_content)
        else:
            print(f"Standard upload for report ({content_size_mb:.2f}MB)")
            success = await create_wiki_page_async(report_title, enhanced_content)
        
        if success:
            # Update index page
            await update_wiki_index_async(report_title, report_slug)
            # Output final access URL
            print(f"Full repository review report is available at: {wiki_url}")
    
    if not success:
        sys.exit(1)

def main():
    """Entry point that runs the async main function"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()