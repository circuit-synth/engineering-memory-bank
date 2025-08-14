#!/usr/bin/env node

/**
 * Memory Bank MCP Server
 * 
 * Model Context Protocol server providing AI agents with comprehensive
 * engineering decision documentation and analysis capabilities.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from '@modelcontextprotocol/sdk/types.js';

class MemoryBankMCPServer {
  private server: Server;

  constructor() {
    this.server = new Server(
      {
        name: 'memory-bank',
        version: '0.0.1',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupHandlers();
  }

  private setupHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'init_memory_bank',
            description: 'Initialize memory-bank system in a project',
            inputSchema: {
              type: 'object',
              properties: {
                project_path: {
                  type: 'string',
                  description: 'Path to project directory',
                  default: '.',
                },
                project_name: {
                  type: 'string',
                  description: 'Name of the project',
                },
              },
            },
          },
          {
            name: 'log_decision',
            description: 'Log an engineering decision with rationale and context',
            inputSchema: {
              type: 'object',
              properties: {
                category: {
                  type: 'string',
                  description: 'Decision category',
                  enum: [
                    'component_selection',
                    'architecture', 
                    'power_supply',
                    'fabrication',
                    'testing',
                    'issue',
                    'milestone',
                    'other'
                  ],
                },
                decision: {
                  type: 'string',
                  description: 'The decision that was made',
                },
                rationale: {
                  type: 'string',
                  description: 'Why this decision was made',
                },
                alternatives: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Alternative options that were considered',
                },
                impact: {
                  type: 'string',
                  enum: ['low', 'medium', 'high', 'critical'],
                  description: 'Impact level of the decision',
                  default: 'medium',
                },
                tags: {
                  type: 'array', 
                  items: { type: 'string' },
                  description: 'Tags for categorization',
                },
                context: {
                  type: 'object',
                  description: 'Additional context information',
                },
              },
              required: ['category', 'decision'],
            },
          },
          {
            name: 'search_decisions',
            description: 'Search decision history by query, category, or tags',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query string',
                },
                category: {
                  type: 'string',
                  description: 'Filter by decision category',
                },
                tags: {
                  type: 'array',
                  items: { type: 'string' },
                  description: 'Filter by tags',
                },
              },
              required: ['query'],
            },
          },
          {
            name: 'analyze_decisions',
            description: 'Get AI-powered analysis of project decisions',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'get_recommendations',
            description: 'Get AI recommendations based on decision history',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'get_timeline',
            description: 'Get chronological timeline of decisions',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'get_statistics',
            description: 'Get memory-bank statistics and metrics',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
          {
            name: 'setup_git_hooks',
            description: 'Setup git hooks for automatic decision capture',
            inputSchema: {
              type: 'object',
              properties: {},
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        // Execute Python command via subprocess
        const result = await this.executePythonCommand(name, args || {});
        
        return {
          content: [
            {
              type: 'text',
              text: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
            },
          ],
        };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        
        return {
          content: [
            {
              type: 'text',
              text: `Error executing ${name}: ${errorMessage}`,
            },
          ],
          isError: true,
        };
      }
    });
  }

  private async executePythonCommand(command: string, params: Record<string, unknown>): Promise<any> {
    // This would execute the Python MCP interface
    // For now, return mock response
    return {
      success: true,
      message: `Executed ${command} with memory-bank`,
      command,
      params
    };
  }

  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
  }
}

// Start the server
const server = new MemoryBankMCPServer();
server.start().catch(console.error);