// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0
import React from "react";

import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools";

export interface SchemaEditorProps {
  jsonSchema: string;
  onChange?: (e: string) => void;
}

/**
 * @param onChange function to be called when the schema is changed
 * @param jsonSchema the schema to be displayed
 * @returns Component for creating a schema editor. Built with react-ace.
 */
export const SchemaEditor: React.FC<SchemaEditorProps> = ({
  onChange,
  jsonSchema,
}) => {
  return (
    <>
      <AceEditor
        mode="json"
        width={"100%"}
        highlightActiveLine={true}
        tabSize={2}
        theme="github"
        value={jsonSchema}
        readOnly={!onChange}
        onChange={onChange}
        showPrintMargin={false}
        name="SCHEMA EDITOR"
        editorProps={{ $blockScrolling: true }}
        setOptions={{
          enableBasicAutocompletion: true,
          enableLiveAutocompletion: true,
          enableSnippets: true,
          showLineNumbers: true,
          tabSize: 2,
          useWorker: false,
        }}
      />
    </>
  );
};
