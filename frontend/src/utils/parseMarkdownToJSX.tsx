import { JSX } from 'react';
import { marked } from 'marked';

const parseMarkdownToJSX = (markdownText: string): JSX.Element => {
  // Convert Markdown to HTML using marked
  const html = marked.parse(markdownText);

  // Return as JSX with dangerouslySetInnerHTML
  return (
    <div
      dangerouslySetInnerHTML={{ __html: html }}
      style={{
        lineHeight: '1.6',
        marginTop: '20px',
      }}
    />
  );
};

export default parseMarkdownToJSX;