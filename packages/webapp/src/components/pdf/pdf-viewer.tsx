// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import { ZoomIn, ZoomOut } from '@material-ui/icons';
import { Button, HeadingStripe, Inline, LoadingIndicator, makeStyles, NORTHSTAR_COLORS, Paper } from 'aws-northstar';
import Grid from 'aws-northstar/layouts/Grid';
import React, { useCallback, useRef, useState } from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import { TransformWrapper, TransformComponent } from 'react-zoom-pan-pinch';


export type DrawingFunction = (ctx: CanvasRenderingContext2D, dimensions: { width: number; height: number }) => void;
export type DrawWrapper = (draw: DrawingFunction) => void;

export interface PdfViewerProps {
  readonly url: string;
  readonly pageNumber: number;
  readonly setPageNumber: (pageNumber: number) => void;
  readonly onPageRenderSuccess?: () => void;
  readonly drawRef?: React.MutableRefObject<DrawWrapper>;
}

// Expand the pdf by this factor when rendered by the pdf viewer, such that it draws at a higher resolution.
// We then zoom out by this factor too so that the pdf renders at the same size on the page. A higher number means more
// pixels and a higher quality.
const QUALITY_SCALE_FACTOR = 2.5;

const useStyles = makeStyles(() => ({
  pdfViewerWrapper: {
    // Set the width of the transform wrapper to 100% so the full pdf area is utilised for zooming/panning
    '& > div': {
      width: '100%',
    },
  },
  pdfViewer: {
    '&:hover': {
      cursor: 'grab',
    },
    '&:hover:active': {
      cursor: 'grabbing',
    },
    'transform': `scale(${1 / QUALITY_SCALE_FACTOR})`,
    'transformOrigin': 'top left',
    '& > div': {
      width: '100%',
    },
  },
}));

/**
 * Component for displaying a pdf document
 */
export const PdfViewer: React.FC<PdfViewerProps> = ({ url, onPageRenderSuccess, drawRef, pageNumber, setPageNumber }) => {
  const [numPages, setNumPages] = useState<number>(0);

  // Reference to the canvas
  const canvas = useRef<HTMLCanvasElement>();

  // Whether or not we should pause drawing while waiting for a page to render
  const isWaitingForPageRender = useRef<boolean>(false);

  // This ref is used to store the current page's "clean" canvas as a data url, allowing us to reset the page prior to
  // painting on top of it
  const cleanCanvasDataUrl = useRef<string>();
  // Cache images to prevent the need to reload them
  const cleanCanvasImages = useRef<{[pageNumber: number]: HTMLImageElement}>({});

  // Allow users of this component to draw on the pdf by providing a drawing function ref. We use this wrapper approach
  // so that the parent component may choose to draw at any time, while allowing this component to block drawing
  // at an unsafe time (ie the transition between pages).
  // This also resets the pdf canvas to a clean page prior to every drawing.
  const drawWrapper = useCallback((draw: DrawingFunction) => {
    // Return when it's unsafe to draw
    if (!canvas.current || !cleanCanvasDataUrl.current || isWaitingForPageRender.current) {
      return;
    }
    const ctx = canvas.current.getContext('2d');
    if (!ctx) {
      return;
    }

    const { width, height } = canvas.current;

    // Use a cached image if available
    const img = cleanCanvasImages.current[pageNumber] || new Image();
    img.onload = null;

    const doDraw = () => {
      ctx.save();

      // Reset the canvas prior to drawing by drawing the clean page
      ctx.drawImage(img, 0, 0);

      draw(ctx, { width, height });

      ctx.restore();
    };

    if (cleanCanvasImages.current[pageNumber]) {
      doDraw();
    } else {
      img.onload = doDraw;
      img.src = cleanCanvasDataUrl.current;
      cleanCanvasImages.current[pageNumber] = img;
    }
  }, [pageNumber, canvas, cleanCanvasImages, cleanCanvasDataUrl, isWaitingForPageRender]);

  if (drawRef) {
    drawRef.current = drawWrapper;
  }

  // Set the number of pages when the document loads
  const onDocumentLoadSuccess = useCallback((pdf: any) => {
    setNumPages(pdf.numPages);
  }, []);

  const onRenderSuccess = useCallback(() => {
    // Whenever a page is rendered by the pdf viewer, take a snapshot of the canvas before we dirty it with our drawings
    cleanCanvasDataUrl.current = canvas.current?.toDataURL();

    // Page has rendered so it's safe to draw again
    isWaitingForPageRender.current = false;
    onPageRenderSuccess && onPageRenderSuccess();
  }, [onPageRenderSuccess]);

  const showPrevPage = useCallback(() => {
    if (pageNumber > 1) {
      isWaitingForPageRender.current = true;
      setPageNumber(pageNumber - 1);
    }
  }, [pageNumber, setPageNumber]);

  const showNextPage = useCallback(() => {
    if (pageNumber < numPages) {
      isWaitingForPageRender.current = true;
      setPageNumber(pageNumber + 1);
    }
  }, [pageNumber, numPages, setPageNumber]);

  const pdfButtons = (
    <Inline>
      <Button label='prev' onClick={showPrevPage}>Prev</Button>
      <Button label='next' onClick={showNextPage}>Next</Button>
    </Inline>
  );

  const styles = useStyles();

  return (
    <>
      <HeadingStripe title={`Page ${pageNumber} of ${numPages}`} actionButtons={pdfButtons} />
      <Grid container spacing={1}>
        <Grid item xs={12}>
          <Paper variant='outlined' style={{ width: '100%', backgroundColor: NORTHSTAR_COLORS.GREY_200 }}>
            <div className={styles.pdfViewerWrapper}>
              <TransformWrapper
                minScale={0.8}
                initialScale={1}
              >
                {({ zoomIn, zoomOut }) => (
                  <div>
                    <div style={{ width: '100%' }}>
                      <div style={{ marginLeft: 'auto', marginRight: 0, width: 'fit-content' }}>
                        <Inline>
                          <Button variant="icon" icon={ZoomOut} onClick={() => zoomOut()} />
                          <Button variant="icon" icon={ZoomIn} onClick={() => zoomIn()} />
                        </Inline>
                      </div>
                    </div>
                    <div style={{ height: canvas.current ? canvas.current.height / QUALITY_SCALE_FACTOR : '70vh' }}>
                      <TransformComponent>
                        <div className={styles.pdfViewer}>
                          <Document
                            file={url}
                            onLoadSuccess={onDocumentLoadSuccess}
                            loading={(
                              <div style={{ transform: `scale(${QUALITY_SCALE_FACTOR})`, transformOrigin: 'top left' }}>
                                <LoadingIndicator />
                              </div>
                            )}
                          >
                            <Page
                              canvasRef={canvas as any}
                              pageNumber={pageNumber}
                              onRenderSuccess={onRenderSuccess}
                              scale={QUALITY_SCALE_FACTOR}
                            />
                          </Document>
                        </div>
                      </TransformComponent>
                    </div>
                  </div>
                )}
              </TransformWrapper>
            </div>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
};
