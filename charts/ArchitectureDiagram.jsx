import React from 'react';
import { motion } from 'framer-motion';
import { 
  Monitor, 
  Database, 
  Cpu, 
  Network,
  FileText,
  Image as ImageIcon,
  Languages,
  Download
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';

const ArchitectureDiagram = () => {
  const components = [
    {
      id: 'ui',
      title: 'User Interface Layer',
      description: 'Tkinter-based desktop application',
      icon: Monitor,
      position: { x: 50, y: 10 },
      color: 'bg-blue-500',
      connections: ['controller']
    },
    {
      id: 'controller',
      title: 'Application Controller',
      description: 'TranslatorApp class managing UI and backend',
      icon: Cpu,
      position: { x: 50, y: 30 },
      color: 'bg-green-500',
      connections: ['pdf', 'ocr', 'translator', 'image']
    },
    {
      id: 'pdf',
      title: 'PDF Processing',
      description: 'PyMuPDF (fitz) for PDF manipulation',
      icon: FileText,
      position: { x: 20, y: 60 },
      color: 'bg-purple-500',
      connections: ['image']
    },
    {
      id: 'ocr',
      title: 'OCR Engine',
      description: 'Pytesseract for text extraction',
      icon: ImageIcon,
      position: { x: 50, y: 60 },
      color: 'bg-orange-500',
      connections: ['translator']
    },
    {
      id: 'translator',
      title: 'Translation Service',
      description: 'Google Translate API via deep_translator',
      icon: Languages,
      position: { x: 80, y: 60 },
      color: 'bg-red-500',
      connections: ['image']
    },
    {
      id: 'image',
      title: 'Image Processing',
      description: 'PIL for image manipulation and reconstruction',
      icon: ImageIcon,
      position: { x: 35, y: 85 },
      color: 'bg-indigo-500',
      connections: ['output']
    },
    {
      id: 'output',
      title: 'Output Generation',
      description: 'PDF creation and file saving',
      icon: Download,
      position: { x: 65, y: 85 },
      color: 'bg-teal-500',
      connections: []
    }
  ];

  const libraries = [
    { name: 'tkinter', purpose: 'GUI Framework', category: 'UI' },
    { name: 'PyMuPDF (fitz)', purpose: 'PDF Processing', category: 'Document' },
    { name: 'PIL (Pillow)', purpose: 'Image Processing', category: 'Graphics' },
    { name: 'pytesseract', purpose: 'OCR Engine', category: 'AI/ML' },
    { name: 'deep_translator', purpose: 'Translation API', category: 'AI/ML' },
    { name: 'threading', purpose: 'Concurrency', category: 'System' }
  ];

  const dataFlow = [
    { from: 'ui', to: 'controller', label: 'User Input' },
    { from: 'controller', to: 'pdf', label: 'PDF File' },
    { from: 'pdf', to: 'image', label: 'Page Images' },
    { from: 'image', to: 'ocr', label: 'Image Data' },
    { from: 'ocr', to: 'translator', label: 'Extracted Text' },
    { from: 'translator', to: 'image', label: 'Translated Text' },
    { from: 'image', to: 'output', label: 'Processed Images' },
    { from: 'output', to: 'controller', label: 'Status Updates' },
    { from: 'controller', to: 'ui', label: 'Progress/Preview' }
  ];

  return (
    <div className="w-full max-w-7xl mx-auto p-6">
      {/* Architecture Diagram */}
      <div className="mb-12">
        <h3 className="text-2xl font-bold text-center mb-8">System Architecture</h3>
        <div className="relative bg-gray-50 rounded-lg p-8 min-h-96">
          <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 1 }}>
            {/* Connection lines */}
            {components.map(component => 
              component.connections.map(targetId => {
                const target = components.find(c => c.id === targetId);
                if (!target) return null;
                
                return (
                  <motion.line
                    key={`${component.id}-${targetId}`}
                    x1={`${component.position.x}%`}
                    y1={`${component.position.y}%`}
                    x2={`${target.position.x}%`}
                    y2={`${target.position.y}%`}
                    stroke="#94a3b8"
                    strokeWidth="2"
                    strokeDasharray="5,5"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 2, delay: 0.5 }}
                  />
                );
              })
            )}
          </svg>
          
          {/* Component nodes */}
          {components.map((component, index) => {
            const Icon = component.icon;
            return (
              <motion.div
                key={component.id}
                className="absolute transform -translate-x-1/2 -translate-y-1/2"
                style={{ 
                  left: `${component.position.x}%`, 
                  top: `${component.position.y}%`,
                  zIndex: 2
                }}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                whileHover={{ scale: 1.1 }}
              >
                <Card className="w-48 shadow-lg hover:shadow-xl transition-shadow">
                  <CardHeader className="pb-2">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${component.color} text-white mx-auto mb-2`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <CardTitle className="text-sm text-center">{component.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="pt-0">
                    <CardDescription className="text-xs text-center">
                      {component.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Libraries and Dependencies */}
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-xl font-bold mb-4">Key Libraries & Dependencies</h3>
          <div className="space-y-3">
            {libraries.map((lib, index) => (
              <motion.div
                key={lib.name}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="flex items-center justify-between p-3 bg-white rounded-lg border"
              >
                <div>
                  <div className="font-semibold text-sm">{lib.name}</div>
                  <div className="text-xs text-gray-600">{lib.purpose}</div>
                </div>
                <div className={`px-2 py-1 rounded text-xs font-medium ${
                  lib.category === 'UI' ? 'bg-blue-100 text-blue-800' :
                  lib.category === 'Document' ? 'bg-green-100 text-green-800' :
                  lib.category === 'Graphics' ? 'bg-purple-100 text-purple-800' :
                  lib.category === 'AI/ML' ? 'bg-orange-100 text-orange-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {lib.category}
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="text-xl font-bold mb-4">Data Flow</h3>
          <div className="space-y-3">
            {dataFlow.map((flow, index) => {
              const fromComponent = components.find(c => c.id === flow.from);
              const toComponent = components.find(c => c.id === flow.to);
              
              return (
                <motion.div
                  key={`${flow.from}-${flow.to}`}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="flex items-center p-3 bg-white rounded-lg border"
                >
                  <div className="flex items-center space-x-2 flex-1">
                    <div className="text-sm font-medium">{fromComponent?.title}</div>
                    <div className="text-gray-400">→</div>
                    <div className="text-sm font-medium">{toComponent?.title}</div>
                  </div>
                  <div className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
                    {flow.label}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArchitectureDiagram;

