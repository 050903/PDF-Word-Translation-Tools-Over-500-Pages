import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FileText, Zap, Languages, Eye, Download, Settings, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';
import WorkflowDiagram from './components/WorkflowDiagram.jsx';
import ArchitectureDiagram from './components/ArchitectureDiagram.jsx';
import TechnicalDocumentation from './components/TechnicalDocumentation.jsx';
import './App.css';

// Navigation Component
const Navigation = () => {
  return (
    <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <FileText className="h-8 w-8 text-blue-600" />
            <span className="text-xl font-bold text-gray-900">PDF Translator</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#overview" className="text-gray-700 hover:text-blue-600 transition-colors">Overview</a>
            <a href="#workflow" className="text-gray-700 hover:text-blue-600 transition-colors">Workflow</a>
            <a href="#features" className="text-gray-700 hover:text-blue-600 transition-colors">Features</a>
            <a href="#architecture" className="text-gray-700 hover:text-blue-600 transition-colors">Architecture</a>
            <a href="#documentation" className="text-gray-700 hover:text-blue-600 transition-colors">Documentation</a>
          </div>
        </div>
      </div>
    </nav>
  );
};

// Hero Section
const HeroSection = () => {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            PDF Translation Tool
            <span className="block text-blue-600">How It Works</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Discover the inner workings of our advanced PDF translation system that combines OCR, 
            machine translation, and visual reconstruction to create seamlessly translated documents.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Zap className="w-4 h-4 mr-2" />
              OCR Technology
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Languages className="w-4 h-4 mr-2" />
              Multi-language Support
            </Badge>
            <Badge variant="secondary" className="px-4 py-2 text-sm">
              <Eye className="w-4 h-4 mr-2" />
              Visual Reconstruction
            </Badge>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

// Overview Section
const OverviewSection = () => {
  return (
    <section id="overview" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            System Overview
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Our PDF translation tool is a sophisticated desktop application built with Python that 
            transforms PDF documents by extracting text through OCR, translating it, and reconstructing 
            the visual layout with translated content. The system leverages multiple advanced technologies 
            to provide accurate, efficient, and user-friendly document translation capabilities.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
          >
            <Card className="h-full hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle>Input Processing</CardTitle>
                <CardDescription>
                  Converts PDF pages to high-resolution images for accurate text detection using PyMuPDF 
                  with configurable DPI settings to balance quality and performance.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <Card className="h-full hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                  <Languages className="w-6 h-6 text-green-600" />
                </div>
                <CardTitle>Translation Engine</CardTitle>
                <CardDescription>
                  Uses advanced OCR via Tesseract and Google Translate API for accurate text extraction 
                  and translation, with intelligent caching to optimize performance.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
          >
            <Card className="h-full hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                  <Download className="w-6 h-6 text-purple-600" />
                </div>
                <CardTitle>Output Generation</CardTitle>
                <CardDescription>
                  Reconstructs the document with translated text while preserving original layout 
                  using PIL image processing and intelligent text fitting algorithms.
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        </div>

        {/* Detailed Process Description */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="bg-gray-50 rounded-lg p-8"
        >
          <h3 className="text-2xl font-bold mb-6">How the Translation Process Works</h3>
          <div className="prose prose-lg max-w-none text-gray-700">
            <p className="mb-4">
              The PDF translation tool operates through a sophisticated multi-stage process that ensures 
              both accuracy and visual fidelity. When a user initiates translation, the system first 
              converts each PDF page into a high-resolution image using PyMuPDF's pixmap functionality. 
              This conversion is crucial because it allows the OCR engine to work with a consistent 
              image format regardless of the original PDF's internal structure.
            </p>
            <p className="mb-4">
              The OCR phase employs Tesseract, one of the most advanced open-source OCR engines available. 
              Tesseract not only extracts the text content but also provides precise bounding box coordinates 
              for each detected text region. This spatial information is essential for maintaining the 
              document's visual layout during reconstruction. The system supports multiple languages 
              simultaneously, enabling it to handle multilingual documents effectively.
            </p>
            <p>
              During the translation phase, the system leverages Google Translate's API through the 
              deep_translator library. To optimize performance and reduce API costs, the system implements 
              an intelligent caching mechanism that stores previously translated text blocks. This approach 
              is particularly effective for documents with repetitive content or standardized formatting.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

// Features Section
const FeaturesSection = () => {
  const features = [
    {
      icon: Settings,
      title: "Quality Control",
      description: "Adjustable DPI settings for balancing processing speed and output quality, with options ranging from 150 DPI for fast processing to 300 DPI for high-quality results."
    },
    {
      icon: Eye,
      title: "Live Preview",
      description: "Real-time visualization of translation progress with page-by-page preview, allowing users to monitor the process and see results as they're generated."
    },
    {
      icon: Zap,
      title: "Smart Caching",
      description: "Translation cache system to avoid re-translating identical text blocks, significantly improving performance for documents with repetitive content."
    },
    {
      icon: Languages,
      title: "Multi-language",
      description: "Support for multiple target languages including Vietnamese, English, Japanese, Korean, and Chinese, with automatic source language detection."
    }
  ];

  return (
    <section id="features" className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
            Key Features
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Advanced capabilities that make our PDF translation tool both powerful and user-friendly, 
            designed to handle complex documents while maintaining ease of use.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <Card className="h-full text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="w-8 h-8 text-blue-600" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription className="text-sm">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Main App Component
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-white">
        <Navigation />
        <HeroSection />
        <OverviewSection />
        <FeaturesSection />
        
        {/* Interactive Workflow Section */}
        <section id="workflow" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Translation Workflow
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Follow the step-by-step process of how our PDF translation tool transforms documents 
                through six distinct phases, each optimized for accuracy and efficiency.
              </p>
            </motion.div>
            <WorkflowDiagram />
          </div>
        </section>

        {/* Interactive Architecture Section */}
        <section id="architecture" className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                System Architecture
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Explore the technical components and data flow of our translation system, 
                built on a modular architecture that ensures scalability and maintainability.
              </p>
            </motion.div>
            <ArchitectureDiagram />
          </div>
        </section>

        {/* Technical Documentation Section */}
        <section id="documentation" className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="text-center mb-12"
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6 flex items-center justify-center gap-3">
                <BookOpen className="w-8 h-8 text-blue-600" />
                Technical Documentation
              </h2>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Comprehensive technical specifications, implementation details, and performance 
                analysis for developers and system administrators.
              </p>
            </motion.div>
            <TechnicalDocumentation />
          </div>
        </section>
      </div>
    </Router>
  );
}

export default App;

