import React from 'react';
import { motion } from 'framer-motion';
import { FileText, Code, Cpu, Database, Network, Zap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx';

const TechnicalDocumentation = () => {
  const technicalSpecs = [
    {
      category: "Core Technologies",
      items: [
        { name: "Python", version: "3.x", purpose: "Main programming language" },
        { name: "Tkinter", version: "Built-in", purpose: "GUI framework for desktop application" },
        { name: "PyMuPDF (fitz)", version: "Latest", purpose: "PDF document processing and manipulation" },
        { name: "PIL (Pillow)", version: "Latest", purpose: "Image processing and manipulation" },
        { name: "pytesseract", version: "Latest", purpose: "OCR engine wrapper for Tesseract" },
        { name: "deep_translator", version: "Latest", purpose: "Translation API wrapper" }
      ]
    },
    {
      category: "System Requirements",
      items: [
        { name: "Operating System", version: "Windows/Linux/macOS", purpose: "Cross-platform compatibility" },
        { name: "Python Runtime", version: "3.7+", purpose: "Minimum Python version required" },
        { name: "Tesseract OCR", version: "4.0+", purpose: "External OCR engine dependency" },
        { name: "Memory", version: "4GB RAM", purpose: "Minimum for processing large PDFs" },
        { name: "Storage", version: "100MB+", purpose: "Application and temporary files" }
      ]
    },
    {
      category: "Performance Metrics",
      items: [
        { name: "Processing Speed", version: "1-3 pages/min", purpose: "Depends on DPI and complexity" },
        { name: "OCR Accuracy", version: "85-95%", purpose: "Varies by document quality" },
        { name: "Translation Quality", version: "Google Translate", purpose: "Depends on language pair" },
        { name: "Memory Usage", version: "200-500MB", purpose: "Per document being processed" },
        { name: "Supported Languages", version: "100+", purpose: "Via Google Translate API" }
      ]
    }
  ];

  const codeExamples = [
    {
      title: "OCR Text Extraction",
      language: "python",
      code: `# Extract text and bounding boxes using Tesseract
ocr_data = pytesseract.image_to_data(
    img, 
    output_type=pytesseract.Output.DICT, 
    lang='eng+vie'
)

# Process each detected text block
for i in range(len(ocr_data['level'])):
    if int(ocr_data['conf'][i]) > 60:  # Confidence threshold
        text = ocr_data['text'][i].strip()
        x, y, w, h = (
            ocr_data['left'][i], 
            ocr_data['top'][i], 
            ocr_data['width'][i], 
            ocr_data['height'][i]
        )`
    },
    {
      title: "Text Translation with Caching",
      language: "python",
      code: `# Translation with cache optimization
if text in translation_cache:
    translated_text = translation_cache[text]
else:
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text)
        translation_cache[text] = translated_text
    except Exception:
        translated_text = text  # Fallback to original`
    },
    {
      title: "Image Reconstruction",
      language: "python",
      code: `# Clear original text area and draw translated text
draw.rectangle(box, fill='white', outline='white')

# Smart text wrapping and font sizing
while font_size > 5:
    font = ImageFont.truetype(font_path, size=font_size)
    if total_text_height <= box_height:
        draw.text((x, y), translated_text, font=font, fill='black')
        break
    font_size -= 1`
    }
  ];

  return (
    <div className="w-full max-w-7xl mx-auto p-6 space-y-12">
      {/* Technical Specifications */}
      <section>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mb-8"
        >
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <Cpu className="w-6 h-6 text-blue-600" />
            Technical Specifications
          </h3>
          <p className="text-gray-600 mb-6">
            Detailed technical requirements and performance characteristics of the PDF translation system.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {technicalSpecs.map((spec, index) => (
            <motion.div
              key={spec.category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <Card className="h-full">
                <CardHeader>
                  <CardTitle className="text-lg">{spec.category}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {spec.items.map((item, itemIndex) => (
                      <div key={itemIndex} className="border-b border-gray-100 pb-2 last:border-b-0">
                        <div className="flex justify-between items-start">
                          <div className="font-medium text-sm">{item.name}</div>
                          <div className="text-xs text-blue-600 font-mono">{item.version}</div>
                        </div>
                        <div className="text-xs text-gray-600 mt-1">{item.purpose}</div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Code Examples */}
      <section>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mb-8"
        >
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <Code className="w-6 h-6 text-green-600" />
            Implementation Examples
          </h3>
          <p className="text-gray-600 mb-6">
            Key code snippets demonstrating the core functionality of the translation system.
          </p>
        </motion.div>

        <div className="space-y-6">
          {codeExamples.map((example, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">{example.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{example.code}</code>
                  </pre>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Performance Analysis */}
      <section>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mb-8"
        >
          <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <Zap className="w-6 h-6 text-yellow-600" />
            Performance Considerations
          </h3>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Optimization Strategies</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-sm mb-2">Translation Caching</h4>
                <p className="text-sm text-gray-600">
                  Implements a dictionary-based cache to store translated text blocks, 
                  preventing redundant API calls for identical content.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm mb-2">Threaded Processing</h4>
                <p className="text-sm text-gray-600">
                  Uses Python threading to keep the UI responsive during long-running 
                  translation operations.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm mb-2">Adaptive Font Sizing</h4>
                <p className="text-sm text-gray-600">
                  Dynamically adjusts font size to fit translated text within original 
                  bounding boxes while maintaining readability.
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Limitations & Challenges</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h4 className="font-semibold text-sm mb-2">OCR Accuracy</h4>
                <p className="text-sm text-gray-600">
                  Performance depends heavily on document quality, font types, and image resolution. 
                  Handwritten or stylized text may have lower accuracy.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm mb-2">Layout Preservation</h4>
                <p className="text-sm text-gray-600">
                  Complex layouts with overlapping elements or non-standard text positioning 
                  may not be perfectly preserved.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-sm mb-2">Processing Speed</h4>
                <p className="text-sm text-gray-600">
                  Higher DPI settings improve quality but significantly increase processing time 
                  and memory usage.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default TechnicalDocumentation;

