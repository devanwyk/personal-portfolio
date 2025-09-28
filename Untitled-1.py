"""Connect model with mcp tools in Python
# Run this python script
> pip install mcp openai
> python <this-script-path>.py
"""
import asyncio
import json
import os
from typing import Dict, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

from openai import OpenAI

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self._servers = {}
        self._tool_to_server_map = {}
        self.exit_stack = AsyncExitStack()
        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        self.openai = OpenAI(
            base_url = "https://models.github.ai/inference",
            api_key = os.environ["GITHUB_TOKEN"],
            default_query = {
                "api-version": "2024-08-01-preview",
            },
        )

    async def connect_stdio_server(self, server_id: str, command: str, args: list[str], env: Dict[str, str]):
        """Connect to an MCP server using STDIO transport
        
        Args:
            server_id: Unique identifier for this server connection
            command: Command to run the MCP server
            args: Arguments for the command
            env: Optional environment variables
        """
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()
        
        # Register the server
        await self._register_server(server_id, session)
    
    async def connect_sse_server(self, server_id: str, url: str, headers: Dict[str, str]):
        """Connect to an MCP server using SSE transport
        
        Args:
            server_id: Unique identifier for this server connection
            url: URL of the SSE server
            headers: Optional HTTP headers
        """
        sse_context = await self.exit_stack.enter_async_context(sse_client(url=url, headers=headers))
        read, write = sse_context
        session = await self.exit_stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        
        # Register the server
        await self._register_server(server_id, session)
    
    async def _register_server(self, server_id: str, session: ClientSession):
        """Register a server and its tools in the client
        
        Args:
            server_id: Unique identifier for this server
            session: Connected ClientSession
        """
        # List available tools
        response = await session.list_tools()
        tools = response.tools
        
        # Store server connection info
        self._servers[server_id] = {
            "session": session,
            "tools": tools
        }
        
        # Update tool-to-server mapping
        for tool in tools:
            self._tool_to_server_map[tool.name] = server_id
            
        print(f"\nConnected to server '{server_id}' with tools:", [tool.name for tool in tools])

    async def chatWithTools(self, messages: list[any]) -> str:
        """Chat with model and using tools
        Args:
            messages: Messages to send to the model
        """
        if not self._servers:
            raise ValueError("No MCP servers connected. Connect to at least one server first.")

        # Collect tools from all connected servers
        available_tools = []
        for server_id, server_info in self._servers.items():
            for tool in server_info["tools"]:
                available_tools.append({ 
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    },
                })

        while True:

            # Call model
            response = self.openai.chat.completions.create(
                messages = messages,
                model = "openai/gpt-4o",
                tools=available_tools,
                response_format = {
                    "type": "text"
                },
                temperature = 1,
                top_p = 1,
            )
            hasToolCall = False

            if response.choices[0].message.tool_calls:
                for tool in response.choices[0].message.tool_calls:
                    hasToolCall = True
                    tool_name = tool.function.name
                    tool_args = json.loads(tool.function.arguments)
                    messages.append({
                        "role": "assistant", 
                        "tool_calls": [{
                            "id": tool.id,
                            "type": "function",
                            "function": {
                                "name": tool.function.name,
                                "arguments": tool.function.arguments,
                            }
                        }]
                    })
                
                    # Find the appropriate server for this tool
                    if tool_name in self._tool_to_server_map:
                        server_id = self._tool_to_server_map[tool_name]
                        server_session = self._servers[server_id]["session"]
                        
                        # Execute tool call on the appropriate server
                        result = await server_session.call_tool(tool_name, tool_args)
                        print(f"[Server '{server_id}' call tool '{tool_name}' with args {tool_args}]: {result.content}")

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool.id,
                            "content": result.content,
                        })
            else:
                messages.append({
                    "role": "assistant",
                    "content": response.choices[0].message.content
                })
                print(f"[Model Response]: {response.choices[0].message.content}")
        
            if not hasToolCall:
                break
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()
        await asyncio.sleep(1)

async def main():
    client = MCPClient()
    messages = [
        {
            "role": "system",
            "content": "You are an advanced web automation specialist with deep expertise in browser automation, web scraping, and user experience analysis. You utilize Playwright tools for comprehensive browser control and are capable of optimizing automated workflows while adhering to ethical and performant practices.\r\n\r\n# Instructions\r\nYour tasks include automating web interactions such as navigation, data extraction, and user interface analysis. Always ensure compliance with website terms of use and respect website-specific limitations. The Playwright tools should be employed to their full capability for efficient and accurate operations. For each task, provide detailed reasoning and execution logs.\r\n\r\n# Steps\r\n1. **Initialization**:\r\n   - Navigate to the provided website using the Playwright `browser_navigate` tool with the given URL.\r\n2. **Ethics and Compliance**:\r\n   - Verify that your actions comply with ethical guidelines and terms of use of the website.\r\n   - Limit navigation or scraping to acceptable rates and avoid triggering security mechanisms.\r\n3. **Advanced Automation Tasks**:\r\n   - Implement content scraping using `browser_evaluate` for DOM inspection and dynamic content handling.\r\n   - Handle pagination efficiently using tools like `browser_click` for buttons or `browser_press_key` for scrolling.\r\n   - Extract and validate structured data (e.g., tables, lists, forms) ensuring no duplication or missing records.\r\n4. **User Experience Analysis**:\r\n   - Capture page load speeds or render times using relevant tools (`browser_snapshot`, network requests checks).\r\n   - Evaluate accessibility features such as ARIA roles or alt-texts.\r\n   - Analyze interaction patterns like hovering, drag-and-drop, or pop-up behavior.\r\n5. **Error Handling and Adaptation**:\r\n   - Manage unexpected website elements like captcha, pop-ups, or broken links using Playwright’s dialog handling capabilities (`browser_handle_dialog`).\r\n   - Retry failed operations where feasible with appropriate delays.\r\n6. **Execution Logging and Reporting**:\r\n   - Generate detailed logs including timestamps, actions performed, tool usage descriptions, and outcomes.\r\n   - Summarize completed tasks and highlight discrepancies, ethical considerations, and user experience findings.\r\n\r\n# Tool Use Guidelines\r\n- Utilize Playwright tools effectively for advanced browser automation tasks:\r\n  - Action tools: `browser_click`, `browser_fill_form`, `browser_drag`, `browser_hover`.\r\n  - Navigation tools: `browser_navigate`, `browser_navigate_back`, `browser_wait_for`.\r\n  - User experience tools: `browser_snapshot`, `browser_network_requests`, `browser_console_messages`.\r\n  - Data extraction and validation tools: `browser_evaluate` for executing JavaScript or inspecting DOM elements.\r\n- When handling complex pages:\r\n  - Use `browser_wait_for` to wait for essential page elements to load.\r\n  - Use `browser_snapshot` for visual or accessibility assessments of the page.\r\n  - Capture network requests through `browser_network_requests` to assess web performance metrics.\r\n\r\n# Examples\r\n\r\n### Example 1: Advanced Pagination and Data Validation\r\n**Input**: A URL for extracting job listings across a dynamic, multi-page website.  \r\n**Process**:\r\n   - Navigate to the homepage.\r\n   - Detect dynamic pagination using `browser_click` or by observing network requests when pages load.\r\n   - Extract and validate job listing entries using `browser_evaluate`. Ensure no duplicate or missing entries.\r\n**Output**:  \r\n- JSON log of the navigation process and structured data summarizing validated job listings.\r\n\r\n### Example 2: User Experience Metrics\r\n**Input**: Analyze user interactions and load performance for a web product page.  \r\n**Process**:\r\n   - Navigate to the page and evaluate load time via captured network requests (`browser_network_requests`).\r\n   - Assess accessibility features using `browser_snapshot` to detect ARIA roles and alt text.\r\n   - Log how hovering over the product image triggers details using `browser_hover` and events captured via `browser_console_messages`.\r\n**Output**:  \r\n- Summary and action log of evaluated accessibility features and performance.\r\n\r\n# Output Format\r\n1. **Execution Logs**: \r\n   - `actions`: Array of steps performed including:\r\n     - `timestamp`: Time of execution.\r\n     - `action`: Description of the executed tool action.\r\n     - `tool`: Name of the tool applied.\r\n     - `details`: Specific parameters or observed results.\r\n   - `errors`: A record of all issues encountered.\r\n2. **Final Result**:\r\n   - Summarized task outcome including user experience findings where applicable.\r\n   - Fully validated and structured extracted data.\r\n\r\nExample JSON structure:\r\n```json\r\n{\r\n  \"actions\": [\r\n    {\r\n      \"timestamp\": \"2023-01-01T12:00:00Z\",\r\n      \"action\": \"Navigate to the homepage\",\r\n      \"tool\": \"browser_navigate\",\r\n      \"details\": { \"url\": \"https://example.com\", \"status\": \"success\" }\r\n    },\r\n    {\r\n      \"timestamp\": \"2023-01-01T12:01:00Z\",\r\n      \"action\": \"Inspect ARIA roles via evaluation\",\r\n      \"tool\": \"browser_evaluate\",\r\n      \"details\": { \"key\": \"accessibility_check\", \"status\": \"success\" }\r\n    }\r\n  ],\r\n  \"errors\": [\r\n    { \"timestamp\": \"2023-01-01T12:02:00Z\", \"error\": \"Timeout waiting for button\", \"remediation\": \"Retry with longer wait time\" }\r\n  ],\r\n  \"result\": {\r\n    \"summary\": \"Accessibility features detected with ARIA roles; load time optimized to 3 seconds.\",\r\n    \"data\": [\r\n      { \"id\": 1, \"title\": \"First Item\", \"details\": \"Details for the first item\" }\r\n    ]\r\n  }\r\n}\r\n```",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Navigate to tradingeconomics.com and gather top 10 economic metrics and history for South Africa such as GDP, Unemployment, Interest Rate, etc in a way such one can view historical performance and create a report that include",
                },
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "\nGoal:\nAutomate extraction of key South African economic metrics from TradingEconomics.com and output structured data.\n\nSteps:\nNavigate & Identify\nGo to the site and locate South Africa’s economic indicators.\nCompliance Check\nRespect site terms and scraping limits.\nLimit to 10 latest records per metric.\nExtract Metrics\nFocus on:\nGDP Growth Rate\nUnemployment Rate\nInterest Rate\nInflation Rate\nGovernment Debt\nStock Market\nFor each: extract date + value.\nEvaluate UX (Optional)\nNote page load speed and chart accessibility.\nOutput Format\nUse JSON or table. Example:\n{\n  \"country\": \"South Africa\",\n  \"metrics\": [\n    {\n      \"name\": \"GDP Growth Rate\",\n      \"units\": \"%\",\n      \"history\": [\n        {\"date\": \"2023-06-30\", \"value\": 2.3},\n        {\"date\": \"2023-03-31\", \"value\": 2.1}\n      ]\n    }\n  ]\n}",
                },
            ],
        },
    ]
    try:
        await client.connect_stdio_server(
            "mcp-meyezffb", 
            "npx", 
            [
                "-y",
                "@playwright/mcp@latest",
            ],
            {
            }
        )
        await client.chatWithTools(messages)
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())