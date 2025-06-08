import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  FileText, 
  Image as ImageIcon, 
  Eye, 
  Languages, 
  Download, 
  Play, 
  Pause,
  RotateCcw,
  ChevronRight,
  CheckCircle
} from 'lucide-react';
import { Button } from '@/components/ui/button.jsx';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';
import { Badge } from '@/components/ui/badge.jsx';

const WorkflowDiagram = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playInterval, setPlayInterval] = useState(null);

  const steps = [
    {
      id: 1,
      title: "PDF Input",
      description: "User selects PDF file and translation settings",
      icon: FileText,
      color: "bg-blue-500",
      details: "The user interface allows selection of PDF file, target language, and quality settings (DPI)."
    },
    {
      id: 2,
      title: "Page Conversion",
      description: "Convert PDF pages to high-resolution images",
      icon: ImageIcon,
      color: "bg-green-500",
      details: "Each PDF page is converted to a pixmap using PyMuPDF with the selected DPI setting."
    },
    {
      id: 3,
      title: "OCR Processing",
      description: "Extract text and bounding boxes using Tesseract",
      icon: Eye,
      color: "bg-purple-500",
      details: "Pytesseract performs OCR to detect text regions and extract content with coordinate information."
    },
    {
      id: 4,
      title: "Translation",
      description: "Translate extracted text using Google Translate",
      icon: Languages,
      color: "bg-orange-500",
      details: "Text blocks are translated using Google Translate API with caching to avoid duplicate translations."
    },
    {
      id: 5,
      title: "Image Reconstruction",
      description: "Replace original text with translated text",
      icon: ImageIcon,
      color: "bg-red-500",
      details: "Original text areas are cleared and replaced with translated text using PIL drawing functions."
    },
    {
      id: 6,
      title: "PDF Output",
      description: "Save all translated pages as new PDF",
      icon: Download,
      color: "bg-indigo-500",
      details: "All processed images are combined into a new PDF file with translated content."
    }
  ];

  const startAnimation = () => {
    if (isPlaying) {
      clearInterval(playInterval);
      setIsPlaying(false);
      setPlayInterval(null);
    } else {
      setIsPlaying(true);
      const interval = setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= steps.length - 1) {
            clearInterval(interval);
            setIsPlaying(false);
            setPlayInterval(null);
            return 0;
          }
          return prev + 1;
        });
      }, 2000);
      setPlayInterval(interval);
    }
  };

  const resetAnimation = () => {
    if (playInterval) {
      clearInterval(playInterval);
      setPlayInterval(null);
    }
    setIsPlaying(false);
    setCurrentStep(0);
  };

  const goToStep = (stepIndex) => {
    if (playInterval) {
      clearInterval(playInterval);
      setPlayInterval(null);
      setIsPlaying(false);
    }
    setCurrentStep(stepIndex);
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6">
      {/* Controls */}
      <div className="flex justify-center gap-4 mb-8">
        <Button 
          onClick={startAnimation}
          className="flex items-center gap-2"
          variant={isPlaying ? "destructive" : "default"}
        >
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          {isPlaying ? "Pause" : "Play"} Animation
        </Button>
        <Button onClick={resetAnimation} variant="outline" className="flex items-center gap-2">
          <RotateCcw className="w-4 h-4" />
          Reset
        </Button>
      </div>

      {/* Workflow Steps */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {steps.map((step, index) => {
          const Icon = step.icon;
          const isActive = index === currentStep;
          const isCompleted = index < currentStep;
          
          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0.5, scale: 0.95 }}
              animate={{ 
                opacity: isActive ? 1 : (isCompleted ? 0.8 : 0.5),
                scale: isActive ? 1.05 : 1,
                y: isActive ? -5 : 0
              }}
              transition={{ duration: 0.3 }}
              className="relative cursor-pointer"
              onClick={() => goToStep(index)}
            >
              <Card className={`h-full transition-all duration-300 ${
                isActive ? 'ring-2 ring-blue-500 shadow-lg' : 
                isCompleted ? 'ring-1 ring-green-500' : ''
              }`}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center ${step.color} text-white`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    {isCompleted && (
                      <CheckCircle className="w-6 h-6 text-green-500" />
                    )}
                    {isActive && (
                      <motion.div
                        animate={{ scale: [1, 1.2, 1] }}
                        transition={{ duration: 1, repeat: Infinity }}
                        className="w-3 h-3 bg-blue-500 rounded-full"
                      />
                    )}
                  </div>
                  <CardTitle className="text-lg">{step.title}</CardTitle>
                  <CardDescription className="text-sm">
                    {step.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-gray-600">
                    {step.details}
                  </p>
                </CardContent>
              </Card>
              
              {/* Arrow connector */}
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                  <ChevronRight className={`w-6 h-6 ${
                    index < currentStep ? 'text-green-500' : 'text-gray-300'
                  }`} />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Current Step Details */}
      <motion.div
        key={currentStep}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6"
      >
        <div className="flex items-center gap-4 mb-4">
          <div className={`w-16 h-16 rounded-full flex items-center justify-center ${steps[currentStep].color} text-white`}>
            {React.createElement(steps[currentStep].icon, { className: "w-8 h-8" })}
          </div>
          <div>
            <h3 className="text-2xl font-bold text-gray-900">
              Step {currentStep + 1}: {steps[currentStep].title}
            </h3>
            <p className="text-gray-600">
              {steps[currentStep].description}
            </p>
          </div>
        </div>
        <p className="text-gray-700 leading-relaxed">
          {steps[currentStep].details}
        </p>
      </motion.div>

      {/* Progress Bar */}
      <div className="mt-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Progress</span>
          <span>{Math.round(((currentStep + 1) / steps.length) * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-blue-500 h-2 rounded-full"
            initial={{ width: "0%" }}
            animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </div>
  );
};

export default WorkflowDiagram;

